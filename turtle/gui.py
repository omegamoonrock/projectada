"""
Sarah Bien + Ananya Rajgarhia

NOTE: numericStringParser requires pyparsing 
Current features:
  - addition, subtraction, mod, division, multiplication, int division
  - repeat loops
  - break points THEY SEEM TO WORK!!
  - print statements work too
  - eval expr using eval and checking for valid syms only
  - saving and loading of up to 10 diff files (by using keyboard lel)
  - if statements
  - debug mode (using breaks)
  - TODO:
   - self-check on drawing game
   - implement else statements 
   - general variables
   - functions -> does not need to support recursion :D
 
"""

#TODO: add undo, syntax highlighting, test functions
#TODO: make it look like sublime
#TODO: better save and load
#TODO: make constants highlighted, don't make variables highlighted
#TODO: make indent smaller

# Begin writing interpreter for Adaas
from tkinter import *
#from Modules.numericStringParser import NumericStringParser 
from tkinter.scrolledtext import *
import tkinter
import string

# taken from http://www.kosbie.net/cmu/fall-14/15-112/notes/file-and-web-io.py
def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

# taken from http://www.kosbie.net/cmu/fall-14/15-112/notes/file-and-web-io.py
def writeFile(filename, contents, mode="wt"):
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

# helper function that processes mathematical assignment expressions
# let var and val be lists that are all the vars in play
# var is a list of strs that are variable names
# vals is a list of values corresponding to the appropriate index of var
# i is the line number 
def eval_expr(data, expr, var, vals, i):
    try:
        elist = list(expr)
        offset = 0

        # fix formatting -> change % to %%
        for i in range(len(expr)):
            if expr[i] == "%":
                elist.insert(i + offset, "%")
                offset += 1
        expr = "".join(elist)

        for i in range(len(var)):
            if (var[i] in expr):
                temp = expr.replace(var[i], "%d")
                expr = temp % vals[i]
    except Exception as e:
        print("Error:", e)
        data.error = True
        data.err_msg = "invalid variable name - should be %s" % var
        data.err_line = i 
        return None
    # print("expr", expr)
    try:
        safe_syms = "<>/*+-.()%="
        for c in expr:
            if not(c.isspace() or c.isalpha() or c.isdigit() or c in safe_syms):
                data.error = True
                data.err_msg = "math syntax error"
                data.err_line = i
                return None    
        
        return eval(expr)
    except:
        data.error = True
        data.err_msg = "math syntax error"
        data.err_line = i
        return None

def strip_end(s):
    slist = list(s)
    for i in range(len(s), 0, -1):
        if not(slist[i - 1].isspace()):
            break
    return "".join(slist[:i])

# returns list of split lines and new line number
def get_indent_body(data, code_lines, k):
    body = []
    print("get_indent_body")
    print(code_lines)
    print(k < len(code_lines))
    print(len(code_lines[k]) > 0)
    print(code_lines[k][0].isspace())
    while (k < len(code_lines) and len(code_lines[k]) > 0 
           and code_lines[k][0].isspace()):
        start = code_lines[k][0]
        if start == " ":
            code_lines[k] = code_lines[k][4:] # get rid of 4 tabbed spaces
        elif start == "\t":
            code_lines[k] = code_lines[k][1:]
        else:
            print(code_lines[k])
            raise Exception("you missed something")
        body += [strip_end(code_lines[k]), "\n"]
        k += 1
    return body, k

def filter_space(code_lines, debug=False):

    filtered_code = []
    for i in range(len(code_lines)):
        line = code_lines[i]
        if not(line == "" or line.isspace() or line.startswith("#")):
            # if (debug and (i != 0)): # don't add break before first line
            #     debug_line = "break"
            #     if line[0].isspace():
            #         for j in range(len(line)):
            #             if not(line[j].isspace()):
            #                 break
            #         debug_line = line[:j] + debug_line
  
            #     result.append(debug_line)
            #     result.append(line)
            #     if (i == len(code_lines) - 1):
            #         result.append(debug_line) # add extra break at the end
        
            filtered_code.append(strip_end(line))

    if debug:
        result = [filtered_code[0]]
        for i in range(1, len(filtered_code)):
            debug_line = "break"
            if line[0].isspace():
                for j in range(len(line)):
                    if not(line[j].isspace()):
                        break
                debug_line = line[:j] + debug_line
            result.append(debug_line)
            result.append(filtered_code[i])
            if (i == len(filtered_code) - 1):
                result.append(debug_line)
    else:
        result = filtered_code

    print("filter space result")
    print(result)
    return result

# TODO: SUPPORT IF/IF-ELSE; WHILE LOOPS (ugh); HINT SYSTEM
# Sarah - syntax highlighting
# Sarah - fontsize variability
# Sarah - display line numbers
# radial coordinates
# draw image/copy image functionality?? lol
# move them towards: for i in range(5) syntax; final level <- use i
# save code (to file)
# debug mode that lets them step through line by line

#GOALS for next meeting:
# break points!!! + print statements
# if/else
# tutorial: variables (concept of picking up pencil), repeat, print, mod, if else, while, functions(no args no return)

"""
code: a multi-line string of "code" w/ the following constraints:
    -valid variable names include: x, y, color
    -valid function calls include: draw(x, y, color, angle)
    -valid commands: repeat <int>: 
    -mathematical operators supported: ^,+,-,/,| (integer division), *,%,abs, exp, 
                                       and sin, cos, tan (radians)
"""
def interpret(data, code, i=0, color="", repeated=0, x0=0, y0=0, x1=0, y1=0):

    code_lines = code.splitlines()
    n = len(code_lines)
    print("\n".join(code_lines))

    while (i < n):
        line = code_lines[i]
        # print("processing line:", line)
        if line.startswith("x"):
            # if you can't split, then there's a syntax error
            expr = line.split("<-")[1].strip()
            val = eval_expr(data, expr, ["x"], [x1], i)
            if val == None:
                data.error = True
                data.err_msg = "assignment error"
                data.err_line = i 
                return None
            x1 = val

        elif line.startswith("y"):
            # if you can't split, then there's a syntax error
            expr = line.split("<-")[1].strip()
            val = eval_expr(data, expr, ["y"], [y1], i)
            if val == None:
                data.error = True
                data.err_msg = "assignment error"
                data.err_line = i  
                return None # there was an error
            y1 = val

        elif line.startswith("color"):
            # if you can't split, then there's a syntax error
            if (len(line.split("<-")) < 2):
                data.error = True
                data.err_msg = "should be of the form \'color <- black\'"
                data.err_line = i
            color = line.split("<-")[1].strip() 

        elif line.startswith("draw"):
            if color != "none":
                data.to_draw.append((x0, y0, x1, y1, color, i))
            x0 = x1
            y0 = y1
        
        elif line.startswith("if"):
            cond = None
            try: 
                # get contents between parens
                start = line.find("(")
                end = line.find(")")
                expr = line[start + 1:end]
                #DEFINE VAR AND VAL
                cond = eval_expr(data, expr, ["x", "y"], [x1, y1], i)

            except Exception as e:
                print("here!")
                data.error = True
                data.err_msg = str(e)
                print(e)
                data.err_line = i 

            if (cond == None): 
                data.error = True
                data.err_msg = str("Condition not set")
                data.err_line = i 
                return 
            (body, k) = get_indent_body(data, code_lines, i + 1)
            if (cond):
                # (body, k) = get_indent_body(data, code_lines, i + 1)
                print(k)
                print("body: ", body)
                result = interpret(data, "".join(body), 0, color, 0, x0, y0, x1, y1)

                if result == None and data.error: #error occured
                    return 
                (_, break_called, x0, y0, x1, y1, color) = result
                if break_called:
                    # you might want to update the variables 
                    # frame is line number, color, #repeats, and coord vals
                    frame = (i, color, 0, x0, y0, x1, y1)
                    print("appending frame: ", frame)
                    data.frames.append(frame)
                    return (False, True, x0, y0, x1, y1, color)
            else:
                print("not cond")
            i = k - 1

        elif line.startswith("repeat"): 
            # get the number between the end of repeat and before the colon
            # 6 because 6 letters in repeat
            try:
                m = int(line.split(":")[0][len("repeat"):].strip())
            except Exception as e:
                data.error = True
                data.err_msg = str(e)
                data.err_line = i 
                return None
            
            print("before get_indent_body")
            print(i + 1)
            print(code_lines)
            body, k = get_indent_body(data, code_lines, i + 1)
            print("repeat loop body:\n", "".join(body))
            # print(k)
            # never entered the while loop
            if k == i + 1: 
                data.error = True
                data.err_msg = "no content to repeat\n\
(Hint: remember to indent the block\nyou would like to repeat)"
                data.err_line = k 
                return None

            # m - repeated to handle for breakpoints
            for j in range(m - repeated):
    
                if data.frames != []:
                    result = interpret(data, "".join(body), *data.frames.pop())    
                else: 
                    result = interpret(data, "".join(body), 0, color, 0, x0, y0, x1, y1)
                
                if result == None and data.error: # error occured
                    return 
                (terminated, break_called, x0, y0, x1, y1, color) = result
                if break_called:
                    # print("j + 1 = ", j + 1)
                    # print("m = ", m)
                    # print("repeated = ", repeated)
                    if j + 1 > m - repeated:
                        print("we should be exiting the loop")
                        # data.frames.pop() # get rid of whatever was appended when you recursed
                        i = k
                    # if i < n:
                    # OFF BY 1 ERROR - you repeat 1 less times than you want to
                    # frame is line number, color, #repeats, and coord vals
                    # ISSUE: how do we keep track of whether we finished the inner part of the loop?
                    # current solution: return extra bool that indicates whether you terminated or not
                    # if you didn't add any frames, then that means you finished everything
                    # if (len(data.frames) == num_frames - 1): repeated += 1
                    print("terminated: ", terminated)
                    if (terminated): repeated += 1
                    frame = (i, color, repeated, x0, y0, x1, y1)
                    print("appending frame: ", frame)
                    data.frames.append(frame)
                    return (False, True, x0, y0, x1, y1, color)
                

            i = k - 1
            print("i = %d" % k)

        elif line.startswith("print"):
            s = line[len("print("):]
            end = s.find(")")
            s = s[:end]
            # TypeError: not all arguments converted during string formatting
            variables = ["x", "y"]
            vals = [x1, y1]
            for j in range(len(variables)):
                var = variables[j]
                if var in s:
                    s = s.replace(var, "%d") % vals[j]
            # s = s.replace("y", "%d") % y1
            # s = s.replace("color", "%s") % color
            data.print_string.append(s)

        elif line.startswith("break"):
            frame = (i + 1, color, 0, x0, y0, x1, y1)
            print("append frame or not?")
            print("n", n)
            print("i", i)
            if (i + 1) == n:
                print("break in interpret appending:", frame)
                # data.frames.append(frame)
                return (True, True, x0, y0, x1, y1, color)
            data.frames.append(frame)
            return (False, True, x0, y0, x1, y1, color)

        else:
            # print some exception
            print("error:", repr(line))
            data.error = True
            data.err_msg = "invalid starting keyword"
            data.err_line = i 
            return None
    
        i += 1

    return (True, False, x0, y0, x1, y1, color)

def draw_code(canvas, data):

    draw_window_height = data.canvas_height - data.draw_window_margin*2
    cx = data.draw_window_margin + data.draw_window_width/2
    cy = data.draw_window_margin + draw_window_height/2
    for obj in data.to_draw:
        (x0, y0, x1, y1, color, i) = obj
        try:
            # negating y to account for conversion to graphical coordinates
            # to cartesian coordinates
            canvas.create_line(x0 + cx,
                               -y0 + cy, 
                               x1 + cx, 
                               -y1 + cy, fill=color, width=5)
        except Exception as e:
            data.error = True
            data.err_msg = str(e)
            data.err_line = i 

def draw_axes(canvas, data):    
    offset = data.draw_window_margin
    draw_window_height = data.canvas_height - offset*2
    cx = data.draw_window_margin + data.draw_window_width/2
    cy = data.draw_window_margin + draw_window_height/2
    
    # x axis
    canvas.create_line(offset, 
                       cy,
                       offset + data.draw_window_width,
                       cy)

    # divide into chunks of 10 rounded down to the nearest even
    interval = 10
    increments_x = data.draw_window_width//interval//2*2 
    marker_radius = 5
    cx = data.draw_window_margin + data.draw_window_width/2
    cy = data.draw_window_margin + draw_window_height/2
    for i in range(1, int(increments_x//2 + 1)):
        mx = cx + interval*i
        mx_n = cx - interval*i
        my_top = cy - marker_radius
        my_bot = cy + marker_radius
        canvas.create_line(mx, my_top, mx, my_bot)
        canvas.create_line(mx_n, my_top, mx_n, my_bot)

    # draw y axis
    canvas.create_line(cx, data.draw_window_margin, cx, 
                       data.draw_window_margin + draw_window_height)

    increments_y = draw_window_height//interval//2*2
    for i in range(1, int(increments_y//2 + 1)):
        mx_l = cx - marker_radius
        mx_r = cx + marker_radius
        my = cy + interval*i
        my_n = cy - interval*i
        canvas.create_line(mx_l, my, mx_r, my)
        canvas.create_line(mx_l, my_n, mx_r, my_n)

def init_GUI(data):
    data.draw_window_margin = 5
    data.draw_window_width = data.canvas_width-data.draw_window_margin 
    data.draw_window_height = data.canvas_height - data.draw_window_margin
    data.margin = 10
    data.draw_window_cx = data.draw_window_margin + data.draw_window_width/2
    data.draw_window_cy = data.draw_window_margin + data.draw_window_height/2
    data.to_draw = []
    data.axes = False


def init(data):
    init_GUI(data)
    #data.nsp = NumericStringParser()
    data.debug_mode = False
    data.type_mode = False
    data.counter = 0
    data.frames = []
    data.print_string = [] # each string in this list should be separated by new line
    data.help = False
    data.error = False
    data.ver = None
    data.err_line = 0
    data.err_msg = ""
    data.code = """x <- -25
y <- 25
color <- none
draw
y <- -25
color <- black
draw
x<--25
y<-0
draw
x<--5
draw
y<-25
color<-none
draw
y<--25
color<-black
draw
x<-5
y<-25
color<-none
draw
y<--25
color<-blue
draw
"""
    interpret(data, data.code)

def mousePressed(event, data):
    pass
    # widget = str(data.masterframe.winfo_containing(event.x_root, event.y_root))
    # textid = str(data.textbox.winfo_name())
    # if(textid in widget):
    #     data.type_mode = True
    #     data.textbox.enable()
    # else:
    #     data.type_mode = False
    #     data.textbox.disable()

def runcode(data):
    # when you break and then recompile something weird happens
    data.error = False
    data.err_msg = ""
    data.code = data.textbox.get_text()
    data.to_draw = []
    data.frames = []
    data.print_string = []
    code_lines = filter_space(data.code.splitlines(), data.debug_mode)
    data.code = "\n".join(code_lines)
    interpret(data, data.code)
    print("frame post return: ", data.frames)

def savecode(data):
    data.textbox.save(data.ver)
    print("data saved")

def loadcode(data):
    data.textbox.load(data.ver)
    print("data loaded")

def clearcode(data):
    data.textbox.delete()

def toggleaxes(data):
    data.axes = not(data.axes)

def toggledebug(data):
    data.debug_mode = not(data.debug_mode)

def stepdebug(data):
    # TODO: DO STACK TRACE OF RECURSIVE CALLS FOR FOR LOOP
    while len(data.frames) > 0:
        frame = data.frames.pop()
        print("frame:", frame)
        # transfer results from recursive call for next iteration
        result = interpret(data, data.code, *frame)
        if result == None: # an error occured
            data.frames = []
            return 
        (_, break_called, x0, y0, x1, y1, color) = result
        if break_called:
            print("frame post c: ", data.frames)
            return

def keyPressed(event, data):
    data.textbox.color()

def timerFired(data):
    data.counter += 1

def draw_screens(canvas, data):
    canvas.create_rectangle(data.draw_window_margin, data.draw_window_margin,
                            data.canvas_width-data.draw_window_margin, 
                           data.canvas_height, width=3)

    data.console.create_rectangle(data.draw_window_margin, data.draw_window_margin,
                            data.canvas_width-data.draw_window_margin, 
                           data.canvas_height, width=3)

def redrawAll(canvas, data):

    draw_screens(canvas, data)

    if data.debug_mode:
        data.console.create_text(data.draw_window_margin + data.margin,
                           data.draw_window_margin + data.draw_window_height,
                           text="Debug Mode",
                           anchor=SW)
    if data.axes:
        draw_axes(canvas, data)
    
    if data.error:
        err_msg = "Error on line %d: %s" % (data.err_line, data.err_msg)
        data.console.create_text(data.draw_window_margin + data.margin, 
                           data.draw_window_margin + data.margin, 
                           text=err_msg, anchor=NW)
    else:
        draw_code(canvas, data)
        p = "\n".join(data.print_string)
        data.console.create_text(data.draw_window_margin + data.margin,
                           data.draw_window_margin + data.margin,
                           text=p, anchor=NW)

#http://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
class TextLineNumbers(tkinter.Canvas):
    def __init__(self, *args, **kwargs):
        tkinter.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tkinter.Text):
    def __init__(self, *args, **kwargs):
        tkinter.Text.__init__(self, *args, **kwargs)

        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tk widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # generate the event for certain types of commands
                if {([lindex $args 0] in {insert replace delete}) ||
                    ([lrange $args 0 2] == {mark set insert}) || 
                    ([lrange $args 0 1] == {xview moveto}) ||
                    ([lrange $args 0 1] == {xview scroll}) ||
                    ([lrange $args 0 1] == {yview moveto}) ||
                    ([lrange $args 0 1] == {yview scroll})} {

                    event generate  $widget <<Change>> -when tail
                }

                # return the result from the real widget command
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))

class CustomTextBox(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tkinter.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set, font=("Helvetica", "18", "bold"))
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        self.text.tag_configure("global", foreground="purple")
        self.text.tag_configure("keyword", foreground="blue")
        self.text.tag_configure("debug", foreground="red")

        self.globals = ["x", "y", "color"]
        self.keywords = ["if", "while", "repeat", "def"]
        self.debug = ["break", "print"]


    def _on_change(self, event):
        self.linenumbers.redraw()

    def get_text(self):
        text = self.text.get("1.0",'end-1c')
        return text

    def save(self, ver=None):
        contents = self.get_text()
        if ver == None:
            writeFile("code.txt", contents)
        else:
            filename = "code%d.txt" % ver
            writeFile(filename, contents)

    def load(self, ver=None):
        if ver == None:
            contents = readFile("code.txt")
        else:
            filename = "code%d.txt" % ver
            contents = readFile(filename)
        self.enable()
        self.text.insert("end",contents)
    
    def delete(self):
        self.text.delete('1.0', END)

    def disable(self):
        print("disable")
        self.text.configure(state="disabled")

    def enable(self):
        print("enable")
        self.text.configure(state="normal")
        #TODO: fix select text

    def color(self):
        print("the text", self.text.get("1.0", END))
        text = self.text.get("1.0", END)
        r = 1
        c = 0
        #rows start at 1 and columns start at 0 *_*
        #coordinate is row.col
        for line in text.splitlines():
            print(line.split())
            line = line.strip()
            c = 0
            for word in line.split():
                while(c < len(line) and line[c] in string.whitespace):
                    c += 1
                initc = "%d.%d" %(r, c)
                endc = "%d.%d" % (r, c + len(word))
                word = self.text.get(initc, endc)
                c += len(word) #1 for the space

                #remove  old tags
                for tag in self.text.tag_names():
                    self.text.tag_remove(tag, initc, endc)

                #apply tags
                if word in self.globals:
                    self.text.tag_add("global", initc, endc)
                elif word in self.keywords:
                    self.text.tag_add("keyword", initc, endc)
                elif word in self.debug:
                    self.text.tag_add("debug", initc, endc)
            r += 1


def run(width=1500, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        data.console.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    data.textbox_width = width//2
    data.canvas_width = width - data.textbox_width
    data.canvas_height = height//2
    init(data)
    # create the root and the canvas
    root = Tk()
    #master frame = left half of the screen
    data.masterframe = Frame(root, width = width, height= height)
    data.masterframe.pack(side="left")

    data.textbox = CustomTextBox(data.masterframe, width = data.textbox_width, height = height)
    data.textbox.pack(fill="both", expand = True)

    runButton = Button(data.masterframe, text="Run", command= lambda: runcode(data))
    runButton.pack(side="left", padx = 15, pady = 10)

    saveButton = Button(data.masterframe, text="Save", command= lambda: savecode(data))
    saveButton.pack(side="left", padx = 15, pady = 10)

    loadButton = Button(data.masterframe, text="Load", command= lambda: loadcode(data))
    loadButton.pack(side="left", padx = 15, pady = 10)

    clearButton = Button(data.masterframe, text="Clear", command= lambda: clearcode(data))
    clearButton.pack(side="left", padx = 15, pady = 10)

    axesButton = Button(data.masterframe, text="Toggle Axes", command= lambda: toggleaxes(data))
    axesButton.pack(side="left", padx = 15, pady = 10)

    debugButton = Button(data.masterframe, text="Toggle Debug", command= lambda: toggledebug(data))
    debugButton.pack(side="left", padx = 15, pady = 10)

    stepButton = Button(data.masterframe, text="Step", command= lambda: stepdebug(data))
    stepButton.pack(side="left", padx = 15, pady = 10)

    #subframe = right half of the screen
    data.subframe = Frame(root, width = data.canvas_width, height= height)
    data.subframe.pack(side="left")

    canvas = Canvas(data.subframe, width = data.canvas_width, height = data.canvas_height)
    canvas.pack(side="top", fill="both", expand = True)

    data.console = Canvas(data.subframe, width = data.canvas_width, height = data.canvas_height)
    data.console.pack(side="bottom", fill="both", expand = True)

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))    
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(900,600)
