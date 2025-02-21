import pytest
from sar_project.agents.resource_manager_agent import ResourceManagerAgent

class TestResourceManagerAgent:
    @pytest.fixture
    def agent(self):
        return ResourceManagerAgent()
    
    def test_initialization(self, agent):
        assert agent.name == "resource_manager"
        assert agent.role == "Resource Manager"
        assert agent.mission_status == "standby"

    def test_status_update(self, agent):
        response = agent.update_resource("helicopter", "status", "active")
        assert response["status"] == "updated"
        assert agent.get_resource_status("helicopter")["status"] == "active"

    def test_get_resource_status(self, agent):
        agent.resources["helicopter"] = {"status": "available"}
        response = agent.get_resource_status("helicopter")
        assert response["status"] == "available"

    def test_update_resource(self, agent):
        agent.resources["helicopter"] = {"status": "available"}
        response = agent.update_resource("helicopter", "status", "in_use")
        assert response["status"] == "updated"
        assert agent.resources["helicopter"]["status"] == "in_use"

    def test_get_resource_schedule(self, agent):
        agent.resources["helicopter"] = {"schedule": "daily"}
        response = agent.get_resource_schedule("helicopter")
        assert response["schedule"] == "daily"

    def test_identify_resources(self, agent):
        agent.resources = {
            "helicopter": {"status": "available"},
            "boat": {"status": "in_use"}
        }
        response = agent.identify_resources()
        assert "identified_resources" in response

    def test_plan_deployment(self, agent):
        agent.resources = {
            "helicopter": {"available_from": 1},
            "boat": {"available_from": 2}
        }
        plan_details = ["helicopter", "boat"]
        response = agent.plan_deployment(plan_details)
        assert response["soonest_available_plan"] == ["helicopter", "boat"]

    def test_allocate_resources(self, agent):
        agent.resources = {
            "helicopter": {"status": "available"},
            "boat": {"status": "in_use"}
        }
        allocation_details = {"helicopter": "agency1", "boat": "agency2"}
        response = agent.allocate_resources(allocation_details)
        assert "allocated_resources" in response
        assert "unallocated_resources" in response

    def test_track_resources(self, agent):
        agent.resources = {
            "helicopter": {"status": "available", "used_by": "none"},
            "boat": {"status": "in_use", "used_by": "agency1"}
        }
        response = agent.track_resources()
        assert "helicopter" in response
        assert "boat" in response

    def test_consolidate_data(self, agent):
        agent.resources = {"helicopter": {"status": "available"}}
        agent.databases = ["db1"]
        response = agent.consolidate_data()
        assert "resources" in response
        assert "databases" in response

    def test_add_datasource(self, agent):
        response = agent.process_request({"add_datasource": True, "datasource": "db1"})
        assert response["status"] == "added"
        assert "db1" in agent.databases

    def test_list_datasources(self, agent):
        agent.databases = ["db1", "db2"]
        response = agent.process_request({"list_datasources": True})
        assert response["datasources"] == ["db1", "db2"]

    def test_remove_datasource(self, agent):
        agent.databases = ["db1", "db2"]
        response = agent.process_request({"remove_datasource": True, "datasource": "db1"})
        assert response["status"] == "removed"
        assert "db1" not in agent.databases

    def test_process_request(self, agent):
        message = {"get_status": True, "resource": "helicopter"}
        response = agent.process_request(message)
        assert "status" in response