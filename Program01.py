# %%
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
import pandas as pd
# %%
def printInput(InputObject, LineObject, Storeable, ShowPreset, OutputObject):
    InputData = InputObject.get(1.0, "end-1c")
    InputData = pd.DataFrame([x.split(';') for x in InputData.split('\n')])
    tmpCode = ParamToCode(InputData, LineObject.get() , Storeable.get() , ShowPreset.get() )
    OutputObject.delete(1.0,tk.END) # clear the outputtext text widget. 1.0 and tk.END are neccessary. tk implies the tkinter module. If you just want to add text dont incude that line
    OutputObject.insert(tk.END,tmpCode) # insert the entry widget contents in the text widget. tk.END is necessary.      

def ParamToCode(InputData, LineObject, Storeable, Showpreset):
    # Default parameters
    constMaxGroups = 5
    constMaxParameterPerGroups = 5
    # Initialise
    CountedGroups = 0
    FilesPointer = 0
    ParameterName = []
    ParameterAddress = []
    ColumnDef = []
    GroupDef = []
    SVGCode = []
    #-> Parameters
    StoreableDef = 'true' if Storeable== 1 else 'false'
    ShowPresetDef = 'true' if Showpreset == 1 else 'false'
    for iTabs in range(constMaxGroups):
        if FilesPointer > InputData.shape[0] - 1:
            break
        CountedGroups += 1
        lParameterName = ''
        lParameterAddress = ''
        for iParameter in range(constMaxParameterPerGroups):
                if FilesPointer > InputData.shape[0] - 1:
                    break
                if pd.isna(InputData[0][FilesPointer]) or InputData[0][FilesPointer] == '' :
                    FilesPointer += 1
                    break
                if lParameterName != '':
                    lParameterName += ","
                    lParameterAddress += ","
                lParameterName += "\""+ "\'Database\'." + InputData[0][FilesPointer] + "\"" 
                lParameterAddress += "\""+ InputData[0][FilesPointer] + "\"" 
                FilesPointer += 1
        ParameterName.append(lParameterName)
        ParameterAddress.append(lParameterAddress)
        tmpString = "\"src" + str(CountedGroups) +"\"," + "\"label" + str(CountedGroups) +"\"," + "\"value" + str(CountedGroups)+"\""
        ColumnDef.append(tmpString)
        tmpString = "\"tab" + str(CountedGroups) +"\""
        GroupDef.append(tmpString)
    #-> Joining all parameters
    ColumnDef = ','.join(ColumnDef)
    GroupDef = ','.join(GroupDef)
    
    SVGCode.append("[Visualization]")
    SVGCode.append("Database=ASW."+LineObject+";")
    SVGCode.append("name="+LineObject+" Parameters;")
    SVGCode.append("type=TableInput;")
    SVGCode.append("permissions=[\"operate\"];")
    SVGCode.append("icon=recipes;")
    SVGCode.append("maxRows=100;")
    SVGCode.append("columns=["+ColumnDef+"];")
    SVGCode.append("storeable="+StoreableDef+";")
    SVGCode.append("showSelectedPreset="+ShowPresetDef+";")
    for iTabs in range(CountedGroups):
        pointerX = iTabs + 1
        pointerY = iTabs
        SVGCode.append("src"+str(pointerX)+".title=Src"+str(pointerX)+";")
        SVGCode.append("src"+str(pointerX)+".type=text;")
        SVGCode.append("src"+str(pointerX)+".display=true;")
        SVGCode.append("src"+str(pointerX)+".src=["+ParameterAddress[pointerY]+"];")
    for iTabs in range(CountedGroups):
        pointerX = iTabs + 1
        pointerY = iTabs
        SVGCode.append("label"+str(pointerX)+".title=Parameter;")
        SVGCode.append("label"+str(pointerX)+".type=text;")
        SVGCode.append("label"+str(pointerX)+".src=["+ParameterName[pointerY]+"];")
    for iTabs in range(CountedGroups):
        pointerX = iTabs + 1
        pointerY = iTabs
        SVGCode.append("value"+str(pointerX)+".title=Value;")
        SVGCode.append("value"+str(pointerX)+".type=field;")
        SVGCode.append("value"+str(pointerX)+".src="+"%"+"src"+str(pointerX)+"%;")
    SVGCode.append("buttons=[];")
    SVGCode.append("tabs=["+GroupDef+"];")
    for iTabs in range(CountedGroups):
        pointerX = iTabs + 1
        pointerY = iTabs
        SVGCode.append("tab"+str(pointerX)+".title=Parameter "+str(pointerX)+";")
        SVGCode.append("tab"+str(pointerX)+".columns=[\"label"+str(pointerX)+"\",\"value"+str(pointerX)+"\"];")
    SVGCode.append("display=true;")   
    SVGCode = '\n'.join(SVGCode)
    return(SVGCode)

# %%
class MainGui:
    def __init__(self, master=None, translator=None):
        _ = translator
        if translator is None:
            def _(x): return x
        
          # build ui
        self.Main = tk.Tk() if master is None else tk.Toplevel(master)
        self.Main.configure(height=600, width=1000)
        self.Main.geometry("1024x768")
        self.Main.title("BCTB EXT - XML Formater")
        self.ParamStoreable =  tk.BooleanVar()
        self.ParamShowpreset = tk.BooleanVar()
        self.ParamLineName = tk.StringVar()
      
        self.tkFrameLeft = ttk.Frame(self.Main)
        self.tkFrameLeft.configure(height=768, width=200)
        self.tkFrameLeft1 = ttk.Frame(self.tkFrameLeft)
        self.tkFrameLeft1.configure(height=200, width=200)
        self.tkEntryLineName = ttk.Entry(self.tkFrameLeft1, textvariable=self.ParamLineName)
        self.tkEntryLineName.grid(column=1, row=0)
        self.tkEntryLineName.insert(0,"MIX1")
        self.tkLabelLine = ttk.Label(self.tkFrameLeft1)
        self.tkLabelLine.configure(text=_('Line name'))
        self.tkLabelLine.grid(column=0, row=0, sticky="w")
        self.tkLabelStoreable = ttk.Label(self.tkFrameLeft1)
        self.tkLabelStoreable.configure(text=_('Storeable'))
        self.tkLabelStoreable.grid(column=0, row=1, sticky="w")
        self.tkLabelShowPreset = ttk.Label(self.tkFrameLeft1)
        self.tkLabelShowPreset.configure(text=_('Show preset'))
        self.tkLabelShowPreset.grid(column=0, row=2, sticky="w")
        self.tkRadioButtonStoreable = ttk.Checkbutton(self.tkFrameLeft1, variable=self.ParamStoreable)
        self.tkRadioButtonStoreable.grid(column=1, row=1)
        self.tkRadioButtonShowPreset = ttk.Checkbutton(self.tkFrameLeft1, variable=self.ParamShowpreset)
        self.tkRadioButtonShowPreset.grid(column=1, row=2)
        self.tkFrameLeft1.pack(pady=10, side="top")
        self.tkFrameLeft2 = ttk.Frame(self.tkFrameLeft)
        self.tkFrameLeft2.configure(height=200, width=200)
        self.tkButtonConvert = ttk.Button(self.tkFrameLeft2)
        self.tkButtonConvert.configure(text=_('Generate'),command=lambda:printInput(InputObject=self.tkTextInput,
                                                                                    LineObject=self.ParamLineName,
                                                                                    Storeable=self.ParamStoreable, 
                                                                                    ShowPreset=self.ParamShowpreset, 
                                                                                    OutputObject=self.tkTextOutput))
        self.tkButtonConvert.pack(side="top")
        self.tkFrameLeft2.pack(side="top")
        self.tkFrameLeft.pack(
            ipadx=10,
            ipady=10,
            padx=10,
            pady=10,
            side="left")
        self.tkFrameRight = ttk.Frame(self.Main)
        self.tkFrameRight.configure(height=750, width=800)
        self.tkTextInput = tk.Text(self.tkFrameRight)
        self.tkTextInput.configure(height=15, width=100)
        self.tkTextInput.insert(1.0,"PAR1A\nPAR1B\n\nPAR2A")
        self.tkTextInput.pack(ipadx=0, ipady=0, padx=0, pady=0, side="top")
        self.tkTextOutput = tk.Text(self.tkFrameRight)
        self.tkTextOutput.configure(height=35, width=100)
        self.tkTextOutput.pack(side="bottom")
        self.tkFrameRight.pack(side="top")

        # Main widget
        self.mainwindow = self.Main

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = MainGui()
    app.run()
