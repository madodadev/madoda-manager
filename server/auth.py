import os
from pathlib import Path
import json

def auth(key):
    main_path = os.environ.get('mm_main_path', "")
    if not main_path:
        main_path = Path(__file__).parent.parent.absolute()
        print(main_path)
    
    conf_path =  main_path / "assets/mainb_conf.json" 
    conf = json.loads(conf_path.read_text())
    auth_conf = conf.get("auth", 0)
    if auth_conf:
        if key in auth_conf.get("api_keys"):
            return True

    return False