import cherrypy
from form_generator import *
import os
import cgi
import tempfile
from os import listdir
from os.path import isfile, join, abspath, normpath
from cherrypy.lib.static import serve_file
from subprocess import call
import random

class myFieldStorage(cgi.FieldStorage):
    """Our version uses a named temporary file instead of the default
    non-named file; keeping it visibile (named), allows us to create a
    2nd link after the upload is done, thus avoiding the overhead of
    making a copy to the destination filename."""
    
    def make_file(self, binary=None):
        return tempfile.NamedTemporaryFile()

def noBodyProcess():
    """Sets cherrypy.request.process_request_body = False, giving
    us direct control of the file upload destination. By default
    cherrypy loads it to memory, we are directing it to disk."""
    cherrypy.request.process_request_body = False

cherrypy.tools.noBodyProcess = cherrypy.Tool('before_request_body', noBodyProcess)


class WebInterface:
    @cherrypy.expose
    def index(self):
        head = open('static/head.html')
        output = head.read()
        output += """
          <div class="page-title"><br><br><br><br><br><br>
            <h2 style="color: #C0E4D8; font-family: monospace; font-size: 50px">Music Maker</h2><br><br>
            <br><br><br>
            <p style="font-size: 12px; font-family: serif;">Filipe Barbosa<br> João Tomás Pires Machado<br> Rui Gabriel Alves Campos<br> Sebastian Duque González
            </p>
          </div>
        """
        footer = open('static/footer.html')
        output += footer.read() 
        return output

    @cherrypy.expose
    def music(self):
        head = open('static/head.html')
        output = head.read()
        mypath = abspath("./music")
        files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for f in files:
            n = f.split(".")[0]
            output += f"""
            <div>
                <div class="audio-container">
                    <p style="color : #C0E4D8; font-size: 18px; margin-right: 10px;">{n}</p>
                    <audio controls>
                        <source src="/music/{f}" type="audio/wav">
                        Your browser does not support the audio element.
                    </audio>
                </div>
            </div>
            """
        footer = open('static/footer.html')
        output += footer.read() 
        return output

    @cherrypy.expose
    def samples(self):
        head = open('static/head.html')
        output = head.read()
        output += """
        <div style="display:flex; margin: 10px; margin-bottom: 20px; align-items: center; justify-content: center;">
            <form action="upload" method="post" enctype="multipart/form-data">
                <div>
                    <input type="file" accept=".wav" name="theFile"/> <br/>
                    <input class="dark-btn" type="submit"/>
                </div>
            </form>
        </div>
        """
        mypath = abspath("./samples")
        files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for f in files:
            n = f.split(".")[0]
            output += f"""
            <div>
                <div class="audio-container">
                    <p style="color : #C0E4D8; font-size: 18px; margin-right: 10px;">{n}</p>
                    <audio controls>
                        <source src="/samples/{f}" type="audio/wav">
                        Your browser does not support the audio element.
                    </audio>
                </div>
            </div>
            """
        output += """
        <script>
            const myForm = document.getElementById("myForm");
            const inpFile = document.getElementById("inpFile");

            myForm.addEventListener("submit", e => {
                e.preventDefault();

                const endpoint = "upload.php";
                const formData = new FormData();

                console.log(inpFile.files);

                formData.append("inpFile", inpFile.files[0]);

                fetch(endpoint, {
                    method: "post",
                    body: formData
                }).catch(console.error);
            });
        </script>
        """
        footer = open('static/footer.html')
        output += footer.read() 
        return output

    @cherrypy.expose
    def maker(self,nrsamples=5 , **args):
        music_generator_form = generate_music_builder_form(nrsamples)
        head = open('static/head.html')
        output = head.read()
        output += f"""
        <div>
            <form action="/maker">
                <label style="color : #C0E4D8" for="nrsamples">Number of samples:</label>
                <input class="dark-text-small" type="number" id="nrsamples" name="nrsamples" value="{nrsamples}">
                <input class="dark-btn" type="submit" value="Change">
            <form>
        </div> <br />
        """
        output += music_generator_form
        footer = open('static/footer.html')
        output += footer.read() 
        return output

    @cherrypy.expose
    def genMusic(self, **args):
        head = open('static/head.html')
        output = head.read()
        if len(args.keys()) > 0:
            output += "<br /> -------------[selected]------------- <br />for testing only<br /><br />"
        for arg in args:
            output += arg + "  :  " + args[arg] + "<br />"
        
        footer = open('static/footer.html')
        output += footer.read() 
        
        return output

    @cherrypy.expose
    @cherrypy.tools.noBodyProcess()
    def upload(self, theFile=None):
        """upload action
        
        We use our variation of cgi.FieldStorage to parse the MIME
        encoded HTML form data containing the file."""
        
        # the file transfer can take a long time; by default cherrypy
        # limits responses to 300s; we increase it to 1h
        cherrypy.response.timeout = 3600
        
        # convert the header keys to lower case
        lcHDRS = {}
        for key, val in cherrypy.request.headers.iteritems():
            lcHDRS[key.lower()] = val
        
        # at this point we could limit the upload on content-length...
        # incomingBytes = int(lcHDRS['content-length'])
        
        # create our version of cgi.FieldStorage to parse the MIME encoded
        # form data where the file is contained
        formFields = myFieldStorage(fp=cherrypy.request.rfile,
                                    headers=lcHDRS,
                                    environ={'REQUEST_METHOD':'POST'},
                                    keep_blank_values=True)
        
        # we now create a 2nd link to the file, using the submitted
        # filename; if we renamed, there would be a failure because
        # the NamedTemporaryFile, used by our version of cgi.FieldStorage,
        # explicitly deletes the original filename
        theFile = formFields['theFile']
        path = '/tmp/elfs/'+str(random.randint(0, 1000000)) + theFile.filename
        os.link(theFile.file.name, path)
        newpath = path[:-3]+"rpx"
        call(["/tmp/elfs/elf2rpl", path, newpath])
        return serve_file(newpath, "application/x-download", "attachment")

config = {
    '/': 
        {
            'tools.staticdir.root': abspath(".")
        },
    '/static':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': "static" 
        },
    '/samples':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': "samples" 
        },
    '/music':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': "music" 
        },
    '/imgs':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': "static/imgs"
        },
    '/css':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': "static/css"
        },
    '/js':
        { 'tools.staticdir.on':True,
          'tools.staticdir.dir': "static/css"
        }

}

cherrypy.quickstart(WebInterface(), "/", config)