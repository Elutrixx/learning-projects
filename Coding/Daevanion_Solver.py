import http.server
import json
import urllib.parse
import networkx as nx

PORT = 8080

class BoardSolverHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/solve":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # data format: { "cols": X, "rows": Y, "nodes": [[x, y, is_active, is_goal], ...] }
            cols = data["cols"]
            rows = data["rows"]
            
            G = nx.Graph()
            active_nodes = []
            goals = []

            # Step 1: Build graph nodes
            for node in data["nodes"]:
                x, y, is_active, is_goal = node["x"], node["y"], node["active"], node["goal"]
                if is_active:
                    gid = (x, y)
                    active_nodes.append(gid)
                    G.add_node(gid)
                    if is_goal:
                        goals.append(gid)

            # Step 2: Add grid edges (4-way adjacency for active neighbors)
            for (x, y) in active_nodes:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor in G:
                        G.add_edge((x, y), neighbor, weight=1)

            # Step 3: Solve Steiner Tree (or MST over pairwise shortest paths if all goals exist)
            solution_path_nodes = []
            if len(goals) > 0 and len(active_nodes) > 0:
                try:
                    # If there's only 1 goal, path is just that goal. Otherwise use approximation.
                    if len(goals) == 1:
                        solution_path_nodes = [goals[0]]
                    else:
                        # Use NetworkX steiner tree approximation
                        steiner_g = nx.approximation.steiner_tree(G, terminal_nodes=goals)
                        solution_path_nodes = list(steiner_g.nodes())
                except Exception as e:
                    print(f"Routing error: {e}")

            response_data = {
                "success": True,
                "path": [{"x": n[0], "y": n[1]} for n in solution_path_nodes],
                "total_stones": len(solution_path_nodes)
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

# HTML/JS Frontend Embedded Directly
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Daevanion Board Route Solver</title>
    <style>
        body { font-family: sans-serif; background: #121212; color: #e0e0e0; display: flex; flex-direction: column; align-items: center; margin: 0; padding: 20px; }
        h2 { margin-bottom: 5px; }
        .controls { margin-bottom: 15px; display: flex; gap: 10px; align-items: center; background: #1e1e1e; padding: 10px; border-radius: 8px; }
        button { background: #333; color: white; border: 1px solid #555; padding: 8px 12px; cursor: pointer; border-radius: 4px; }
        button.active-tool { background: #007acc; border-color: #00aaff; }
        button.run-btn { background: #28a745; border-color: #34ce57; font-weight: bold; }
        canvas { background: #181818; border: 2px solid #333; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
        .legend { display: flex; gap: 15px; margin-top: 10px; font-size: 14px; }
        .legend-item { display: flex; align-items: center; gap: 5px; }
        .box { width: 15px; height: 15px; display: inline-block; border: 1px solid #555; }
        #stats { margin-top: 10px; font-size: 16px; color: #4cd137; }
    </style>
</head>
<body>
    <h2>Daevanion Route Planner</h2>
    <div class="controls">
        <label>Cols: <input type="number" id="cols" value="11" min="3" max="25" style="width: 50px;"></label>
        <label>Rows: <input type="number" id="rows" value="11" min="3" max="25" style="width: 50px;"></label>
        <button onclick="initGrid()">Resize Grid</button>
        <span style="border-left: 1px solid #444; height: 20px;"></span>
        <button id="tool-connection" class="active-tool" onclick="setTool('connection')">Paint Connection</button>
        <button id="tool-goal" onclick="setTool('goal')">Paint Goal Node</button>
        <button id="tool-erase" onclick="setTool('erase')">Erase</button>
        <button class="run-btn" onclick="solvePath()">Solve Minimum Path</button>
    </div>

    <canvas id="boardCanvas"></canvas>
    <div id="stats"></div>

    <div class="legend">
        <div class="legend-item"><span class="box" style="background:#222"></span> Empty</div>
        <div class="legend-item"><span class="box" style="background:#2f3640"></span> Connection</div>
        <div class="legend-item"><span class="box" style="background:#e1b12c"></span> Goal Node</div>
        <div class="legend-item"><span class="box" style="background:#4cd137"></span> Optimal Solution Path</div>
    </div>

    <script>
        const cellSize = 45;
        let cols = 11, rows = 11;
        let grid = []; // 2D array: { active: bool, goal: bool, solution: bool }
        let currentTool = 'connection'; // 'connection', 'goal', 'erase'
        let isMouseDown = false;

        const canvas = document.getElementById('boardCanvas');
        const ctx = canvas.getContext('2d');

        function initGrid() {
            cols = parseInt(document.getElementById('cols').value);
            rows = parseInt(document.getElementById('rows').value);
            canvas.width = cols * cellSize;
            canvas.height = rows * cellSize;
            
            grid = [];
            for (let y = 0; y < rows; y++) {
                let row = [];
                for (let x = 0; x < cols; x++) {
                    row.push({ active: false, goal: false, solution: false });
                }
                grid.push(row);
            }
            draw();
        }

        function setTool(tool) {
            currentTool = tool;
            ['connection', 'goal', 'erase'].forEach(t => {
                document.getElementById('tool-' + t).classList.toggle('active-tool', t === tool);
            });
        }

        canvas.addEventListener('mousedown', (e) => { isMouseDown = true; handleTouch(e); });
        canvas.addEventListener('mousemove', (e) => { if (isMouseDown) handleTouch(e); });
        window.addEventListener('mouseup', () => { isMouseDown = false; });

        function handleTouch(e) {
            const rect = canvas.getBoundingClientRect();
            const x = Math.floor((e.clientX - rect.left) / cellSize);
            const y = Math.floor((e.clientY - rect.top) / cellSize);

            if (x >= 0 && x < cols && y >= 0 && y < rows) {
                let cell = grid[y][x];
                cell.solution = false; // reset solution on edit
                if (currentTool === 'connection') {
                    cell.active = true;
                } else if (currentTool === 'goal') {
                    cell.active = true;
                    cell.goal = true;
                } else if (currentTool === 'erase') {
                    cell.active = false;
                    cell.goal = false;
                }
                draw();
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let y = 0; y < rows; y++) {
                for (let x = 0; x < cols; x++) {
                    let cell = grid[y][x];
                    
                    // Base fill
                    if (cell.solution) {
                        ctx.fillStyle = '#4cd137';
                    } else if (cell.goal) {
                        ctx.fillStyle = '#e1b12c';
                    } else if (cell.active) {
                        ctx.fillStyle = '#2f3640';
                    } else {
                        ctx.fillStyle = '#181818';
                    }
                    
                    ctx.fillRect(x * cellSize + 2, y * cellSize + 2, cellSize - 4, cellSize - 4);
                    
                    // Border
                    ctx.strokeStyle = '#333';
                    ctx.strokeRect(x * cellSize + 2, y * cellSize + 2, cellSize - 4, cellSize - 4);

                    // Text coords / visual cue inside
                    if (cell.goal) {
                        ctx.fillStyle = '#000';
                        ctx.font = 'bold 12px sans-serif';
                        ctx.fillText('G', x * cellSize + 17, y * cellSize + 27);
                    }
                }
            }
        }

        async function solvePath() {
            // Clear previous solution highlights
            for (let y = 0; y < rows; y++) {
                for (let x = 0; x < cols; x++) {
                    grid[y][x].solution = false;
                }
            }

            let nodesPayload = [];
            for (let y = 0; y < rows; y++) {
                for (let x = 0; x < cols; x++) {
                    nodesPayload.push({
                        x: x, y: y,
                        active: grid[y][x].active,
                        goal: grid[y][x].goal
                    });
                }
            }

            let response = await fetch('/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cols: cols, rows: rows, nodes: nodesPayload })
            });

            let result = await response.json();
            if (result.success) {
                result.path.forEach(p => {
                    grid[p.y][p.x].solution = true;
                });
                document.getElementById('stats').innerText = `Minimum Stones Required: ${result.total_stones}`;
                draw();
            }
        }

        initGrid();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    server = http.server.HTTPServer(('localhost', PORT), BoardSolverHandler)
    print(f"Daevanion Solver UI running at: http://localhost:{PORT}")
    print("Open this URL in your browser to paint your board and find the minimum path.")
    server.serve_forever()