from . import create_app  
import os

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


#RUN TERMINAL;
#(venv) bhupathisaicharan@CBHUPATHI EAPP % cd /Users/bhupathisaicharan/Documents/PROJECTS/ECOMMERS/ECM_BD
#(venv) bhupathisaicharan@CBHUPATHI ECM_BD % source EAPP/venv/bin/activate
#(venv) bhupathisaicharan@CBHUPATHI ECM_BD % python3 -m EAPP.app_runner or EAPP/venv/bin/python3 -m EAPP.app_runner
