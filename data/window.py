import win32gui
def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def get_roblox_HWND():
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if "roblox" in i[1].lower():
            return i[0]
    return -1

def focus_roblox():
    roblox_hwnd = get_roblox_HWND()
    if roblox_hwnd == -1:
        return -1
    win32gui.ShowWindow(roblox_hwnd, 5)
    win32gui.SetForegroundWindow(roblox_hwnd)