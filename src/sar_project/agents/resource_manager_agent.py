from sar_project.agents.base_agent import SARBaseAgent
import json

class ResourceManagerAgent(SARBaseAgent):
    def __init__(self, name="resource_manager"):
        super().__init__(
            name=name,
            role="Resource Manager",
            system_message="""You are the resource manager for SAR operations. Your role is to:
            1. Manage resource schedules
            2. Develop deployment plans
            3. Create priority lists
            4. Coordinate with other team members, namely a People Manager and Asset Manager"""
        )
        self.databases = []  # List to store database connections or data sources
        self.resources = {}
        
    def process_request(self, message):
        """Process resource-related requests"""
        try:
            if "get_status" in message:
                return self.get_resource_status(message["resource"])
            elif "update_status" in message:
                return self.update_resource(message["resource"], "status", message["status"])
            elif "update_schedule" in message:
                return self.update_resource(message["resource"], "schedule", message["schedule"])
            elif "get_schedule" in message:
                return self.get_resource_schedule(message["resource"])
            elif "identify_resources" in message:
                return self.identify_resources()
            elif "plan_deployment" in message:
                return self.plan_deployment(message["plan_details"])
            elif "allocate_resources" in message:
                return self.allocate_resources(message["allocation_details"])
            elif "track_resources" in message:
                return self.track_resources()
            elif "consolidate_data" in message:
                return self.consolidate_data()
            elif "add_datasource" in message:
                self.databases.append(message["datasource"])
                return {"status": "added", "datasource": message["datasource"]}
            elif "list_datasources" in message:
                return {"datasources": self.databases}
            elif "remove_datasource" in message:
                if message["datasource"] in self.databases:
                    self.databases.remove(message["datasource"])
                    return {"status": "removed", "datasource": message["datasource"]}
                else:
                    return {"error": "Datasource not found"}
            else:
                return {"error": "Unknown request type"}
        except Exception as e:
            return {"error": str(e)}
        
    def get_resource_status(self, resource_name):
        """Get status of a specific resource"""
        return self.resources.get(resource_name, {"status": "unknown"})
    
    def update_resource(self, resource_name, field, value):
        """Update a specific field of a resource"""
        self.resources[resource_name][field] = value
        return {"status": "updated", "field": field, "new_value": value}
    
    def get_resource_schedule(self, resource_name):
        """Get schedule for a specific resource"""
        return {"resource": resource_name, "schedule": self.resources.get(resource_name, {}).get("schedule", "unknown")}
    
    def identify_resources(self):
        """Identify available resources"""
        identified_resources = map(self.is_resource_available, self.resources)
        return {"identified_resources": identified_resources}
    
    def plan_deployment(self, plan_details):
        """Plan deployment of resources"""
        # Sort resources by soonest available time
        sorted_resources = sorted(
            plan_details,
            key=lambda resource: self.resources.get(resource, {}).get("available_from", float('inf'))
        )
        deployment_plan = {"soonest_available_plan": sorted_resources}
        return deployment_plan
    
    def allocate_resources(self, allocation_details):
        """Allocate resources based on the provided details"""
        allocated_resources = {}
        unallocated_resources = {}

        for resource, agency in allocation_details.items():
            if self.resources.get(resource, {}).get("status") == "available":
                self.resources[resource]["status"] = "unavailable"
                self.resources[resource]["used_by"] = agency
                allocated_resources[resource] = agency
            else:
                unallocated_resources[resource] = agency

        allocation_result = {
            "allocated_resources": allocated_resources,
            "unallocated_resources": unallocated_resources
        }
        return allocation_result
    
    def track_resources(self):
        """Track the status and location of resources"""
        tracked_resources = {}
        for resource, details in self.resources.items():
            tracked_resources[resource] = {
            "status": details.get("status", "unknown"),
            "used_by": details.get("used_by", "none")
            }
        return tracked_resources
    
    def consolidate_data(self):
        """Consolidate data from various sources and present in JSON format"""
        consolidated_data = {
            "resources": self.resources,
            "databases": self.databases
        }
        return json.dumps(consolidated_data, indent=4)

    def is_resource_available(self, resource):
        """Check if a resource is available for deployment"""
        if self.resources.get(resource, {"status": None})["status"] == "available":
            return resource