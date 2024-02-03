from typing import List
from ninja_extra import NinjaExtraAPI, api_controller, route
from devices.models import Device, Location
from devices.schemas import (
    DeviceCreateSchema,
    DeviceSchema,
    LocationSchema,
    Error,
    DeviceLocationPatch,
)
from django.shortcuts import get_object_or_404

app = NinjaExtraAPI()


@api_controller("devices/", tags=["Devices"], permissions=[])
class DeviceController:
    @route.get("/", response=List[DeviceSchema])
    def get_devices(self):
        return Device.objects.all()

    @route.get("{slug}", response=DeviceSchema)
    def get_device(self, slug: str):
        device = get_object_or_404(Device, slug=slug)
        return device

    @route.post("/", response={200: DeviceSchema, 404: Error})
    def create_device(self, props: DeviceCreateSchema):
        # if `location_id` is given, check to see if it actually exists
        if props.location_id:
            location_exists = Location.objects.filter(id=props.location_id).exists()
            if not location_exists:
                return 404, {
                    "message": f"location_id: {props.location_id} does not exist"
                }
        props = props.model_dump()
        device = Device.objects.create(**props)
        return device

    @route.post("{device_slug}/set-location/", response=DeviceSchema)
    def update_device_location(self, device_slug: str, location: DeviceLocationPatch):
        device = get_object_or_404(Device, slug=device_slug)
        if location.location_id:
            location = get_object_or_404(Location, id=location.location_id)
            device.location = location
        else:
            device.location = None
        device.save()
        return device


@api_controller("locations/", tags=["Locations"], permissions=[])
class LocationsController:
    @route.get("/", response=List[LocationSchema])
    def get_locations(self):
        return Location.objects.all()


app.register_controllers(DeviceController, LocationsController)
