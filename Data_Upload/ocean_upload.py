import ocean

# Get your Ocean API key from your Ocean Protocol account settings.
ocean_api_key = "YOUR_OCEAN_API_KEY"

# Create an Ocean client object.
ocean_client = ocean.client(api_key=ocean_api_key)

# Use the Ocean client object to interact with the Ocean Protocol API.
data_asset = ocean_client().create_data_asset(
    name="My Dataset",
    description="This is a dataset of my data.",
    data_url="https://example.com/my_dataset.zip",
    data_type="image/jpeg",
    price=1.0,
)

# Upload the data asset to Ocean Protocol.
ocean_client().upload_data_asset(data_asset)

# Print the data asset ID.
print(data_asset.id)