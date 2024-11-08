import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from src.graph import Graph
from src.algorithms import bfs, dfs, dijkstra

# Campus Navigation Interface Class
class CampusNavigator:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Navigator")
        self.root.geometry("1200x900")

        # Load campus map and resize for better scaling on macOS
        self.map_image = Image.open("data/map.png")
        self.map_image = self.map_image.resize((800, 800), Image.Resampling.LANCZOS)
        self.map_photo = ImageTk.PhotoImage(self.map_image)

        # Location coordinates on the map for easy reference
        self.locations = {
            "AdmissionsOffice": (524, 723),
            "TitanStore": (335, 520),
            "ClayesPerformanceArtCenter": (357, 609),
            "ComputerScience": (635, 490),
            "DanBlackHall": (375, 711),
            "Engineering": (600, 495),
            "EducationClassroom": (500, 555),
            "EastsideNorthParkingStructure": (730, 570),
            "EastsideSouthParkingStructure": (730, 620),
            "GordonHall": (510, 675),
            "Humanities": (520, 620),
            "Kinesiology": (380, 480),
            "LangsdorfHall": (480, 715),
            "McCarthyHall": (410, 673),
            "NutwoodParkingStructure": (240, 695),
            "PollakLibrary": (425, 530),
            "StudentRecreationCenter": (260, 440),
        }

        # Initialize start and end points for pathfinding
        self.start_point = None
        self.end_point = None

        # Setup the canvas to display the map
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.canvas.create_image(0, 0, anchor="nw", image=self.map_photo)

        self._draw_locations()

        # Load the campus graph for pathfinding algorithms
        self.graph = Graph()
        self.graph.load_from_csv("data/campus.csv")

        # Add control buttons for pathfinding
        self._add_buttons()

        # Label to show path details after computation
        self.path_details = tk.Label(root, text="", font=("Arial", 10), justify="left", wraplength=400)
        self.path_details.grid(row=0, column=2, columnspan=2, pady=20, padx=20)

    def _draw_locations(self):
        """ Draw all location markers on the map with clickable nodes. """
        for loc, (x, y) in self.locations.items():
            node = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="yellow", outline="black", tags="node")
            self.canvas.tag_bind(node, "<Button-1>", lambda event, location=loc: self.select_location(location))
            self.canvas.create_text(x, y-10, text=loc, font=("Arial", 8), fill="red")

    def _add_buttons(self):
        """ Add pathfinding buttons for BFS, DFS, and Dijkstra algorithms. """
        tk.Button(self.root, text="Find Path (BFS)", command=self.find_path_bfs).grid(row=1, column=0)
        tk.Button(self.root, text="Find Path (DFS)", command=self.find_path_dfs).grid(row=1, column=1)
        tk.Button(self.root, text="Find Path (Dijkstra)", command=self.find_path_dijkstra).grid(row=1, column=2)

    def select_location(self, location):
        """ Select and highlight start or end node. """
        if not self.start_point:
            self.start_point = location
            self._highlight_location(location, "blue")
        elif not self.end_point:
            self.end_point = location
            self._highlight_location(location, "pink")
        else:
            self.reset_selection()
            self.start_point = location
            self._highlight_location(location, "blue")

    def _highlight_location(self, location, color):
        """ Helper method to highlight selected location. """
        x, y = self.locations[location]
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline="black", tags="highlight")

    def reset_selection(self):
        """ Reset selected start and end points. """
        self.canvas.delete("path")
        self.canvas.delete("highlight")
        self.start_point = None
        self.end_point = None
        self.path_details.config(text="")

    def find_path_bfs(self):
        """ Execute BFS algorithm to find a path. """
        if self.start_point and self.end_point:
            self._draw_path(bfs)

    def find_path_dfs(self):
        """ Execute DFS algorithm to find a path. """
        if self.start_point and self.end_point:
            self._draw_path(dfs)

    def find_path_dijkstra(self):
        """ Execute Dijkstra algorithm to find a path. """
        if self.start_point and self.end_point:
            self._draw_path(dijkstra)

    def _draw_path(self, algorithm):
        """ Draw path on canvas and show path details. """
        path = algorithm(self.graph, self.start_point, self.end_point)
        self.canvas.delete("path")
        self.path_details.config(text="")

        total_distance = 0
        total_time = 0
        details = []

        if path:
            for i in range(len(path) - 1):
                start, end = path[i], path[i + 1]
                x1, y1 = self.locations[start]
                x2, y2 = self.locations[end]
                self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3, tags="path")

                edge = self.graph.adj_list[start][end]
                distance = edge['distance']
                time = edge['time']
                accessible = "Yes" if edge['accessible'] else "No"
                
                total_distance += distance
                total_time += time
                details.append(f"{start} -> {end}:\n  Distance: {distance} m\n  Time: {time} min\n  Accessible: {accessible}\n")

            details_text = "\n".join(details)
            total_text = f"\nTotal Distance: {total_distance} m\nTotal Time: {total_time} min"
            self.path_details.config(text=details_text + total_text)
            
            x_start, y_start = self.locations[self.start_point]
            x_end, y_end = self.locations[self.end_point]
            self.canvas.create_oval(x_start-5, y_start-5, x_start+5, y_start+5, fill="red", tags="path")
            self.canvas.create_oval(x_end-5, y_end-5, x_end+5, y_end+5, fill="green", tags="path")
        else:
            messagebox.showinfo("Result", "No path found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavigator(root)
    root.mainloop()
