from chimg.config import Config
import json

# generate the JSON schema and write to `json_schema.json`
main_model_schema = Config.model_json_schema()
with open("json_schema.json", "w") as f:
    f.write(json.dumps(main_model_schema, indent=2))