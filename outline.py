import cv2
import numpy as np
import os

points = []
window_name = "Block Outliner (Made by xvoid)"
max_grid_expansion = 10

def mouse_callback(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 3:
            points.append(np.array([x, y], dtype=np.float32))
            print(f"Point {len(points)}: {(x, y)}")
        if len(points) == 3:
            print("3 points selected. Pres d to draw block, r to reset all points.")

def complete_square(pts):
    A, B, C = pts
    D = A + (C - B)
    return np.array([A, B, C, D], dtype=np.float32)

def draw_block_grid(img, square_pts, max_x, max_y):
    vec_x = square_pts[1] - square_pts[0]
    vec_y = square_pts[3] - square_pts[0]

    for i in range(-max_x, max_x + 1):
        for j in range(-max_y, max_y + 1):
            origin = square_pts[0] + i * vec_x + j * vec_y
            corners = np.array([
                origin,
                origin + vec_x,
                origin + vec_x + vec_y,
                origin + vec_y
            ], dtype=np.int32)
            cv2.polylines(img, [corners], isClosed=True, color=(0, 255, 0), thickness=2)

def main():
    global points
    img_path = input("put image path, make sure the image is in the same folder as the python script: ").strip()
    img = cv2.imread(img_path)
    if img is None:
        print("uh oh, read the directions")
        return

    clone = img.copy()

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    print("Instructions:")
    print("- click 3 corners")
    print("- 4th point will be drawn automatically")
    print("- d to draw after 3 points have been set")
    print("- r reset the points")
    print("- q quit the window")

    while True:
        temp_img = clone.copy()
        for pt in points:
            cv2.circle(temp_img, tuple(pt.astype(int)), 5, (0, 0, 255), -1)
        if len(points) == 3:
            square_pts = complete_square(points)
            cv2.polylines(temp_img, [square_pts.astype(np.int32)], isClosed=True, color=(255, 255, 0), thickness=2)
            for i, p in enumerate(square_pts):
                color = (0, 255, 255) if i < 3 else (255, 0, 0)
                cv2.circle(temp_img, tuple(p.astype(int)), 5, color, -1)

        cv2.imshow(window_name, temp_img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            points = []
            print("Points have been reset.")
        elif key == ord('d'):
            if len(points) == 3:
                square_pts = complete_square(points)
                print("Drawing block outlines...")
                draw_block_grid(clone, square_pts, max_grid_expansion, max_grid_expansion)
                cv2.imshow(window_name, clone)

                # Save the result image
                output_path = "output.png"
                cv2.imwrite(output_path, clone)
                print(f"Image saved")
            else:
                print("Give me 3 points to draw grid.")
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
