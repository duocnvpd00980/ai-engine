import json
import httpx
import asyncio
from fastapi import HTTPException

class ComfyCloudService:
    def __init__(self, api_key: str):
        self.base_url = "https://cloud.comfy.org"
        self.headers = {"X-API-Key": api_key, "Content-Type": "application/json"}

    async def generate_image(self, workflow_path: str, replacements: dict):
        with open(workflow_path, "r", encoding="utf-8") as f:
            workflow = json.load(f)

        # Map dữ liệu vào các Node ID (VD: Node "6" cho prompt)
        for node_id, value in replacements.items():
            if node_id in workflow:
                workflow[node_id]["inputs"]["text"] = value

        async with httpx.AsyncClient(follow_redirects=True, timeout=300.0) as client:
            # Gửi Prompt
            res = await client.post(f"{self.base_url}/api/prompt", headers=self.headers, json={"prompt": workflow})
            if res.status_code != 200: raise HTTPException(status_code=500, detail=res.text)
            prompt_id = res.json()["prompt_id"]

            # Polling trạng thái
            while True:
                status_res = await client.get(f"{self.base_url}/api/job/{prompt_id}/status", headers=self.headers)
                status = status_res.json().get("status")
                if status == "completed": break
                if status in ("failed", "cancelled"): raise HTTPException(status_code=500, detail=f"AI Job {status}")
                await asyncio.sleep(3)

            # Lấy ảnh
            hist_res = await client.get(f"{self.base_url}/api/history_v2/{prompt_id}", headers=self.headers)
            outputs = hist_res.json().get("outputs", {})
            for node_id, node_output in outputs.items():
                if "images" in node_output:
                    img = node_output["images"][0]
                    view_res = await client.get(f"{self.base_url}/api/view", headers=self.headers, 
                                               params={"filename": img["filename"], "type": "output"})
                    return view_res.content
        raise HTTPException(status_code=404, detail="No output image")