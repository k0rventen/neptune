import time
from locust import HttpUser, task, between, SequentialTaskSet

class UserTasks(SequentialTaskSet):
    @task
    def wait_api(self):
        while True:
            try:
                all_items = self.client.get("/api")
                break
            except:
                time.sleep(1)
        print("Neptune is ready, starting tests..")

    @task
    def scan_images(self):
        for image in ["k0rventen/macaque"]:
            scanned_image = self.client.post(
                "/api/scan", json={"image": image})
            if scanned_image.status_code == 200:
                print(scanned_image.json())
            else:
                exit(1)

    @task
    def list_vulnerabilities(self):
        all_items = self.client.get("/api/vulnerabilities")
        if all_items.status_code == 200:
            for item in all_items.json()["items"]:
                self.client.get(f"/api/vulnerabilities/{item['id']}")

    @task
    def list_packages(self):
        all_items = self.client.get("/api/packages")
        if all_items.status_code == 200:
            for item in all_items.json()["items"]:
                self.client.get(f"/api/packages/{item['id']}")

    @task
    def list_tags(self):
        all_items = self.client.get("/api/tags")
        if all_items.status_code == 200:
            for item in all_items.json()["items"]:
                self.client.get(f"/api/tags/{item['sha']}")

    @task
    def halt(self):
        print("stopping")
        exit(0)


class APIUser(HttpUser):
    host = "http://neptune:5000"
    wait_time = between(1, 3)
    tasks = [UserTasks]
