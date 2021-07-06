from os import listdir
from os.path import isfile, join, abspath
def generate_music_builder_form(rows = 1):
    output = """<div class="music-maker-form"><form action="/genMusic">"""
    for i in range(int(rows)):
        output += f"""
        <div id=s{i}>
            <select class="opt-dark" id="sample{i}" name="sample{i}">
            """
        mypath = abspath("./samples")
        files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for f in files:
            t = f.split(".")[0]
            output += f"""<option value="{f}">{t}</option>"""
        output +=f"""
            </select>
            <input class="checkbox-fancy" type="checkbox" id="s{i}t1" name="s{i}t1"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t2" name="s{i}t2"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t3" name="s{i}t3"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t4" name="s{i}t4"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t5" name="s{i}t5"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t6" name="s{i}t6"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t7" name="s{i}t7"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t8" name="s{i}t8"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t9" name="s{i}t9"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t10" name="s{i}t10"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t11" name="s{i}t11"> 
            <input class="checkbox-fancy" type="checkbox" id="s{i}t12" name="s{i}t12">
            <select class="opt-dark" id="effect{i}" name="effect{i}">
                <option value="none">None</option>
                <option value="fadein">Fade In</option>
                <option value="fadeout">Fade Out</option>
                <option value="other">Other</option>
            </select> 
        </div>
        """
    output += """
    </div>
        <br />
        <input class="dark-btn" formaction="/genMusic" type="submit" value="Create Music">
    </form><div>
    """ 
    return output












#   <form action="/index">
#       <div id=s1>
#           <input type="checkbox" id="s1t1" name="s1t1"> 
#           <input type="checkbox" id="s1t2" name="s1t2"> 
#           <input type="checkbox" id="s1t3" name="s1t3"> 
#           <input type="checkbox" id="s1t4" name="s1t4"> 
#           <input type="checkbox" id="s1t5" name="s1t5"> 
#           <input type="checkbox" id="s1t6" name="s1t6"> 
#           <input type="checkbox" id="s1t7" name="s1t7"> 
#           <input type="checkbox" id="s1t8" name="s1t8"> 
#           <input type="checkbox" id="s1t9" name="s1t9"> 
#           <input type="checkbox" id="s1t10" name="s1t10"> 
#           <input type="checkbox" id="s1t11" name="s1t11"> 
#           <input type="checkbox" id="s1t12" name="s1t12"> 
#       </div>
#           <input type="submit" value="Create Sound">
#   </form>