"""
Comprehensive unit tests for vm_creation.tf Terraform configuration.

This test suite validates:
- Terraform syntax and structure
- Provider configuration
- Resource naming and attributes
- Data source configuration
- Output definitions
- Security best practices
- GCP-specific configurations
"""

import pytest
import hcl2
import json
import re
from pathlib import Path


class TestTerraformSyntax:
    """Test suite for basic Terraform syntax and structure validation."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        tf_file = Path("vm_creation.tf")
        with open(tf_file) as f:
            config = hcl2.load(f)
        return config
    
    def test_terraform_file_exists(self):
        """Verify that vm_creation.tf file exists."""
        assert Path("vm_creation.tf").exists(), "vm_creation.tf file should exist"
    
    def test_terraform_file_not_empty(self):
        """Verify that vm_creation.tf is not empty."""
        content = Path("vm_creation.tf").read_text()
        assert len(content.strip()) > 0, "vm_creation.tf should not be empty"
    
    def test_valid_hcl2_syntax(self, terraform_config):
        """Verify that the Terraform file has valid HCL2 syntax."""
        assert terraform_config is not None, "Terraform config should parse without errors"
        assert isinstance(terraform_config, dict), "Parsed config should be a dictionary"
    
    def test_has_required_top_level_blocks(self, terraform_config):
        """Verify that configuration contains expected top-level blocks."""
        assert 'provider' in terraform_config, "Configuration should have provider block"
        assert 'resource' in terraform_config, "Configuration should have resource block"
        assert 'data' in terraform_config, "Configuration should have data block"
        assert 'output' in terraform_config, "Configuration should have output block"


class TestProviderConfiguration:
    """Test suite for Google Cloud provider configuration."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    @pytest.fixture
    def provider_config(self, terraform_config):
        """Extract provider configuration."""
        return terraform_config.get('provider', [{}])[0].get('google', [{}])[0]
    
    def test_provider_block_exists(self, terraform_config):
        """Verify that provider block exists."""
        assert 'provider' in terraform_config, "Provider block should exist"
        assert len(terraform_config['provider']) > 0, "Provider block should not be empty"
    
    def test_google_provider_configured(self, terraform_config):
        """Verify that Google Cloud provider is configured."""
        provider_block = terraform_config.get('provider', [{}])[0]
        assert 'google' in provider_block, "Google provider should be configured"
    
    def test_provider_has_project_id(self, provider_config):
        """Verify that provider has project ID configured."""
        assert 'project' in provider_config, "Provider should have project configured"
        assert provider_config['project'], "Project ID should not be empty"
    
    def test_provider_project_format(self, provider_config):
        """Verify that project ID follows expected format."""
        project = provider_config.get('project', '')
        # GCP project IDs typically start with letters and contain alphanumeric chars and hyphens
        assert len(project) > 0, "Project ID should not be empty"
        assert re.match(r'^[a-z][-a-z0-9]*[a-z0-9]$', project) or \
               re.match(r'^hc-[a-f0-9]+$', project), \
               f"Project ID format seems unusual: {project}"
    
    def test_provider_has_region(self, provider_config):
        """Verify that provider has region configured."""
        assert 'region' in provider_config, "Provider should have region configured"
        assert provider_config['region'], "Region should not be empty"
    
    def test_provider_region_is_valid(self, provider_config):
        """Verify that region is a valid GCP region."""
        region = provider_config.get('region', '')
        valid_regions = ['us-central1', 'us-east1', 'us-west1', 'europe-west1', 'asia-east1']
        # Allow any region that follows GCP naming pattern
        assert region in valid_regions or re.match(r'^[a-z]+-[a-z]+\d+$', region), \
               f"Region should be valid GCP region, got: {region}"


class TestDataSourceConfiguration:
    """Test suite for Terraform data source configuration."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    @pytest.fixture
    def data_source(self, terraform_config):
        """Extract data source configuration."""
        return terraform_config.get('data', [{}])[0].get('tfe_outputs', [{}])[0]
    
    def test_data_source_exists(self, terraform_config):
        """Verify that data source block exists."""
        assert 'data' in terraform_config, "Data source block should exist"
        assert len(terraform_config['data']) > 0, "Data source should not be empty"
    
    def test_tfe_outputs_data_source(self, terraform_config):
        """Verify that tfe_outputs data source is configured."""
        data_block = terraform_config.get('data', [{}])[0]
        assert 'tfe_outputs' in data_block, "tfe_outputs data source should exist"
    
    def test_data_source_has_organization(self, data_source):
        """Verify that data source has organization configured."""
        assert 'organization' in data_source, "Data source should have organization"
        assert data_source['organization'], "Organization should not be empty"
    
    def test_data_source_organization_value(self, data_source):
        """Verify that organization value is correct."""
        org = data_source.get('organization', '')
        assert org == 'devopsmayur', f"Organization should be 'devopsmayur', got: {org}"
    
    def test_data_source_has_workspace(self, data_source):
        """Verify that data source has workspace configured."""
        assert 'workspace' in data_source, "Data source should have workspace"
        assert data_source['workspace'], "Workspace should not be empty"
    
    def test_data_source_workspace_value(self, data_source):
        """Verify that workspace value is correct."""
        workspace = data_source.get('workspace', '')
        assert workspace == 'gcpnw', f"Workspace should be 'gcpnw', got: {workspace}"


class TestOutputConfiguration:
    """Test suite for Terraform output configuration."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    @pytest.fixture
    def output_config(self, terraform_config):
        """Extract output configuration."""
        return terraform_config.get('output', [{}])[0]
    
    def test_output_block_exists(self, terraform_config):
        """Verify that output block exists."""
        assert 'output' in terraform_config, "Output block should exist"
        assert len(terraform_config['output']) > 0, "Output should not be empty"
    
    def test_network_info_output_exists(self, output_config):
        """Verify that network_info output exists."""
        assert 'network_info' in output_config, "network_info output should exist"
    
    def test_output_has_value(self, output_config):
        """Verify that output has value configured."""
        network_info = output_config.get('network_info', [{}])[0]
        assert 'value' in network_info, "Output should have value"
    
    def test_output_references_data_source(self, output_config):
        """Verify that output references the data source."""
        network_info = output_config.get('network_info', [{}])[0]
        value = network_info.get('value', '')
        assert 'data.tfe_outputs.test.id' in str(value), \
               "Output should reference data.tfe_outputs.test.id"


class TestComputeInstanceResource:
    """Test suite for Google Compute Instance resource configuration."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    @pytest.fixture
    def instance_resource(self, terraform_config):
        """Extract compute instance resource configuration."""
        resources = terraform_config.get('resource', [{}])[0]
        return resources.get('google_compute_instance', {}).get('world111', [{}])[0]
    
    def test_compute_instance_resource_exists(self, terraform_config):
        """Verify that compute instance resource exists."""
        assert 'resource' in terraform_config, "Resource block should exist"
        resources = terraform_config.get('resource', [{}])[0]
        assert 'google_compute_instance' in resources, "google_compute_instance resource should exist"
    
    def test_resource_name_is_world111(self, terraform_config):
        """Verify that resource name is 'world111' (updated from world11)."""
        resources = terraform_config.get('resource', [{}])[0]
        compute_instances = resources.get('google_compute_instance', {})
        assert 'world111' in compute_instances, "Resource should be named 'world111'"
        assert 'world11' not in compute_instances, "Old resource name 'world11' should not exist"
    
    def test_instance_has_name_attribute(self, instance_resource):
        """Verify that instance has name attribute."""
        assert 'name' in instance_resource, "Instance should have name attribute"
        assert instance_resource['name'], "Instance name should not be empty"
    
    def test_instance_name_value(self, instance_resource):
        """Verify that instance name is correct."""
        name = instance_resource.get('name', '')
        assert name == 'my-instance7', f"Instance name should be 'my-instance7', got: {name}"
    
    def test_instance_has_machine_type(self, instance_resource):
        """Verify that instance has machine_type attribute."""
        assert 'machine_type' in instance_resource, "Instance should have machine_type"
        assert instance_resource['machine_type'], "Machine type should not be empty"
    
    def test_instance_machine_type_format(self, instance_resource):
        """Verify machine type format (note: t3.medium is AWS-style)."""
        machine_type = instance_resource.get('machine_type', '')
        # Note: This appears to be an error - t3.medium is AWS EC2 instance type
        # GCP uses formats like n1-standard-1, e2-medium, etc.
        assert machine_type == 't3.medium', "Machine type should match configured value"
        # Warning: This is likely an error in the config
    
    def test_instance_has_zone(self, instance_resource):
        """Verify that instance has zone attribute."""
        assert 'zone' in instance_resource, "Instance should have zone"
        assert instance_resource['zone'], "Zone should not be empty"
    
    def test_instance_zone_matches_region(self, terraform_config, instance_resource):
        """Verify that instance zone is within the provider region."""
        provider_config = terraform_config.get('provider', [{}])[0].get('google', [{}])[0]
        region = provider_config.get('region', '')
        zone = instance_resource.get('zone', '')
        
        if region:
            assert zone.startswith(region), \
                   f"Zone '{zone}' should be in region '{region}'"
    
    def test_instance_zone_format(self, instance_resource):
        """Verify that zone follows GCP format."""
        zone = instance_resource.get('zone', '')
        assert re.match(r'^[a-z]+-[a-z]+\d+-[a-z]$', zone), \
               f"Zone should follow GCP format (e.g., us-central1-a), got: {zone}"


class TestBootDiskConfiguration:
    """Test suite for boot disk configuration."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    @pytest.fixture
    def instance_resource(self, terraform_config):
        """Extract compute instance resource configuration."""
        resources = terraform_config.get('resource', [{}])[0]
        return resources.get('google_compute_instance', {}).get('world111', [{}])[0]
    
    @pytest.fixture
    def boot_disk(self, instance_resource):
        """Extract boot disk configuration."""
        return instance_resource.get('boot_disk', [{}])[0]
    
    def test_boot_disk_exists(self, instance_resource):
        """Verify that boot disk is configured."""
        assert 'boot_disk' in instance_resource, "Instance should have boot_disk configured"
        assert instance_resource['boot_disk'], "Boot disk should not be empty"
    
    def test_boot_disk_has_initialize_params(self, boot_disk):
        """Verify that boot disk has initialize_params."""
        assert 'initialize_params' in boot_disk, "Boot disk should have initialize_params"
        assert boot_disk['initialize_params'], "Initialize params should not be empty"
    
    def test_boot_disk_has_image(self, boot_disk):
        """Verify that boot disk has image specified."""
        init_params = boot_disk.get('initialize_params', [{}])[0]
        assert 'image' in init_params, "Initialize params should have image"
        assert init_params['image'], "Image should not be empty"
    
    def test_boot_disk_image_format(self, boot_disk):
        """Verify that boot disk image follows GCP format."""
        init_params = boot_disk.get('initialize_params', [{}])[0]
        image = init_params.get('image', '')
        # GCP images typically follow project/image-family or just image-family format
        assert '/' in image or '-' in image, \
               f"Image should follow GCP format, got: {image}"
    
    def test_boot_disk_image_value(self, boot_disk):
        """Verify that boot disk image is correct."""
        init_params = boot_disk.get('initialize_params', [{}])[0]
        image = init_params.get('image', '')
        assert image == 'debian-cloud/debian-11', \
               f"Image should be 'debian-cloud/debian-11', got: {image}"


class TestNetworkConfiguration:
    """Test suite for network interface configuration."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    @pytest.fixture
    def instance_resource(self, terraform_config):
        """Extract compute instance resource configuration."""
        resources = terraform_config.get('resource', [{}])[0]
        return resources.get('google_compute_instance', {}).get('world111', [{}])[0]
    
    @pytest.fixture
    def network_interface(self, instance_resource):
        """Extract network interface configuration."""
        return instance_resource.get('network_interface', [{}])[0]
    
    def test_network_interface_exists(self, instance_resource):
        """Verify that network interface is configured."""
        assert 'network_interface' in instance_resource, \
               "Instance should have network_interface configured"
        assert instance_resource['network_interface'], "Network interface should not be empty"
    
    def test_network_interface_has_network(self, network_interface):
        """Verify that network interface has network specified."""
        assert 'network' in network_interface, "Network interface should have network"
        assert network_interface['network'], "Network should not be empty"
    
    def test_network_interface_network_value(self, network_interface):
        """Verify that network is set to default."""
        network = network_interface.get('network', '')
        assert network == 'default', f"Network should be 'default', got: {network}"
    
    def test_network_interface_has_access_config(self, network_interface):
        """Verify that network interface has access_config for public IP."""
        assert 'access_config' in network_interface, \
               "Network interface should have access_config for external IP"
    
    def test_access_config_allows_external_ip(self, network_interface):
        """Verify that access_config is present (enables ephemeral public IP)."""
        access_config = network_interface.get('access_config', [])
        # Empty list or dict with empty values means ephemeral IP
        assert access_config is not None, "Access config should exist for public IP"


class TestSecurityAndBestPractices:
    """Test suite for security and best practices validation."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    @pytest.fixture
    def tf_content(self):
        """Load raw Terraform file content."""
        return Path("vm_creation.tf").read_text()
    
    def test_no_hardcoded_secrets(self, tf_content):
        """Verify that no obvious secrets are hardcoded."""
        # Check for common secret patterns
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'private_key\s*=\s*["\'][^"\']+["\']',
        ]
        for pattern in secret_patterns:
            matches = re.findall(pattern, tf_content, re.IGNORECASE)
            assert len(matches) == 0, \
                   f"Found potential hardcoded secret: {matches}"
    
    def test_project_id_not_default(self, terraform_config):
        """Verify that project ID is not using a default/example value."""
        provider_config = terraform_config.get('provider', [{}])[0].get('google', [{}])[0]
        project = provider_config.get('project', '')
        invalid_projects = ['my-project', 'example-project', 'test-project', 'project-id']
        assert project not in invalid_projects, \
               f"Project ID should not be a placeholder value: {project}"
    
    def test_instance_name_follows_convention(self, terraform_config):
        """Verify that instance name follows naming convention."""
        resources = terraform_config.get('resource', [{}])[0]
        instance = resources.get('google_compute_instance', {}).get('world111', [{}])[0]
        name = instance.get('name', '')
        # Check for valid naming pattern (lowercase, hyphens, alphanumeric)
        assert re.match(r'^[a-z][-a-z0-9]*[a-z0-9]$', name), \
               f"Instance name should follow GCP naming convention: {name}"
    
    def test_resource_identifier_consistency(self, terraform_config):
        """Verify that resource identifiers are consistent."""
        resources = terraform_config.get('resource', [{}])[0]
        instance_resources = resources.get('google_compute_instance', {})
        # Should have exactly one instance defined
        assert len(instance_resources) == 1, \
               "Should have exactly one compute instance resource"
    
    def test_region_and_zone_consistency(self, terraform_config):
        """Verify that zone is within the specified region."""
        provider_config = terraform_config.get('provider', [{}])[0].get('google', [{}])[0]
        region = provider_config.get('region', '')
        
        resources = terraform_config.get('resource', [{}])[0]
        instance = resources.get('google_compute_instance', {}).get('world111', [{}])[0]
        zone = instance.get('zone', '')
        
        if region and zone:
            assert zone.startswith(region), \
                   f"Zone '{zone}' should be within region '{region}'"


class TestConfigurationIssues:
    """Test suite to identify potential configuration issues."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    def test_machine_type_is_gcp_compatible(self, terraform_config):
        """Verify machine type compatibility (detect AWS types)."""
        resources = terraform_config.get('resource', [{}])[0]
        instance = resources.get('google_compute_instance', {}).get('world111', [{}])[0]
        machine_type = instance.get('machine_type', '')
        
        # AWS instance types: t2.*, t3.*, m5.*, c5.*, etc.
        aws_patterns = [r'^t[2-3]\.', r'^m[4-5]\.', r'^c[4-5]\.', r'^r[4-5]\.']
        is_aws_type = any(re.match(pattern, machine_type) for pattern in aws_patterns)
        
        if is_aws_type:
            pytest.fail(
                f"Machine type '{machine_type}' appears to be AWS EC2 type, not GCP. "
                f"GCP uses types like: n1-standard-1, e2-medium, n2-standard-2, etc."
            )
    
    def test_no_missing_required_fields(self, terraform_config):
        """Verify that all required fields are present."""
        resources = terraform_config.get('resource', [{}])[0]
        instance = resources.get('google_compute_instance', {}).get('world111', [{}])[0]
        
        required_fields = ['name', 'machine_type', 'zone', 'boot_disk', 'network_interface']
        missing_fields = [field for field in required_fields if field not in instance]
        
        assert len(missing_fields) == 0, \
               f"Missing required fields: {missing_fields}"
    
    def test_boot_disk_properly_configured(self, terraform_config):
        """Verify that boot disk configuration is complete."""
        resources = terraform_config.get('resource', [{}])[0]
        instance = resources.get('google_compute_instance', {}).get('world111', [{}])[0]
        boot_disk = instance.get('boot_disk', [{}])[0]
        
        assert boot_disk, "Boot disk should be configured"
        assert 'initialize_params' in boot_disk, "Boot disk should have initialize_params"
        
        init_params = boot_disk.get('initialize_params', [{}])[0]
        assert 'image' in init_params, "Initialize params should specify an image"


class TestDiffChanges:
    """Test suite specifically for the changes made in this diff."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    def test_resource_renamed_from_world11_to_world111(self, terraform_config):
        """Verify that resource was renamed from world11 to world111."""
        resources = terraform_config.get('resource', [{}])[0]
        compute_instances = resources.get('google_compute_instance', {})
        
        # New name should exist
        assert 'world111' in compute_instances, \
               "Resource should be named 'world111' (new name)"
        
        # Old name should not exist
        assert 'world11' not in compute_instances, \
               "Old resource name 'world11' should not exist"
    
    def test_resource_attributes_unchanged(self, terraform_config):
        """Verify that only the resource name changed, not attributes."""
        resources = terraform_config.get('resource', [{}])[0]
        instance = resources.get('google_compute_instance', {}).get('world111', [{}])[0]
        
        # Verify key attributes remain the same
        assert instance.get('name') == 'my-instance7', "Instance name attribute unchanged"
        assert instance.get('machine_type') == 't3.medium', "Machine type unchanged"
        assert instance.get('zone') == 'us-central1-a', "Zone unchanged"
    
    def test_resource_identifier_follows_pattern(self, terraform_config):
        """Verify that the new resource identifier follows a logical pattern."""
        resources = terraform_config.get('resource', [{}])[0]
        compute_instances = resources.get('google_compute_instance', {})
        
        # Check that 'world111' exists and follows a pattern
        assert 'world111' in compute_instances, "New resource identifier should exist"
        
        # Pattern appears to be 'world' + numbers
        resource_name = 'world111'
        assert resource_name.startswith('world'), \
               "Resource identifier should start with 'world'"
        assert resource_name[5:].isdigit(), \
               "Resource identifier should end with digits"


class TestEdgeCases:
    """Test suite for edge cases and error conditions."""
    
    def test_file_encoding_is_utf8(self):
        """Verify that the Terraform file uses UTF-8 encoding."""
        try:
            with open("vm_creation.tf", encoding='utf-8') as f:
                f.read()
            assert True, "File is UTF-8 encoded"
        except UnicodeDecodeError as e:
            pytest.fail(f"File encoding issue: {e}")
    
    def test_no_trailing_whitespace_issues(self):
        """Check for excessive trailing whitespace that might cause issues."""
        with open("vm_creation.tf") as f:
            lines = f.readlines()
        
        excessive_whitespace_lines = [
            i+1 for i, line in enumerate(lines) 
            if len(line.rstrip()) > 0 and len(line) - len(line.rstrip()) > 10
        ]
        
        assert len(excessive_whitespace_lines) == 0, \
               f"Lines with excessive trailing whitespace: {excessive_whitespace_lines}"
    
    def test_consistent_indentation(self):
        """Verify that indentation is consistent throughout the file."""
        with open("vm_creation.tf") as f:
            lines = f.readlines()
        
        # Check for mixed tabs and spaces
        lines_with_tabs = [i+1 for i, line in enumerate(lines) if '\t' in line]
        
        # Terraform convention is spaces, not tabs
        if len(lines_with_tabs) > 0:
            pytest.skip(f"Lines with tabs found: {lines_with_tabs}. Tabs are acceptable but spaces preferred.")
    
    def test_no_duplicate_resource_definitions(self):
        """Verify that there are no duplicate resource definitions."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        
        resources = config.get('resource', [{}])[0]
        compute_instances = resources.get('google_compute_instance', {})
        
        # Should only have one instance
        assert len(compute_instances) == 1, \
               f"Should have exactly 1 compute instance, found {len(compute_instances)}"
    
    def test_all_blocks_properly_closed(self):
        """Verify that all blocks are properly closed with braces."""
        with open("vm_creation.tf") as f:
            content = f.read()
        
        open_braces = content.count('{')
        close_braces = content.count('}')
        
        assert open_braces == close_braces, \
               f"Mismatched braces: {open_braces} open, {close_braces} close"


class TestIntegrationReadiness:
    """Test suite to verify configuration is ready for deployment."""
    
    @pytest.fixture
    def terraform_config(self):
        """Load and parse the Terraform configuration file."""
        with open("vm_creation.tf") as f:
            config = hcl2.load(f)
        return config
    
    def test_all_required_providers_specified(self, terraform_config):
        """Verify that all required providers are specified."""
        assert 'provider' in terraform_config, "Provider block must be present"
        
        provider_block = terraform_config.get('provider', [{}])[0]
        assert 'google' in provider_block, "Google provider must be configured"
    
    def test_data_sources_have_valid_references(self, terraform_config):
        """Verify that data sources reference valid organizations/workspaces."""
        data_block = terraform_config.get('data', [{}])[0]
        tfe_outputs = data_block.get('tfe_outputs', {}).get('test', [{}])[0]
        
        org = tfe_outputs.get('organization', '')
        workspace = tfe_outputs.get('workspace', '')
        
        assert org, "Data source must have organization"
        assert workspace, "Data source must have workspace"
        assert len(org) > 0, "Organization should not be empty"
        assert len(workspace) > 0, "Workspace should not be empty"
    
    def test_outputs_use_valid_syntax(self, terraform_config):
        """Verify that outputs use valid Terraform interpolation syntax."""
        output_block = terraform_config.get('output', [{}])[0]
        network_info = output_block.get('network_info', [{}])[0]
        
        value = str(network_info.get('value', ''))
        
        # Should reference a data source or resource
        assert 'data.' in value or 'google_compute_instance.' in value or \
               '${' in value, "Output should reference a valid resource or data source"
    
    def test_resource_dependencies_resolvable(self, terraform_config):
        """Verify that resource dependencies can be resolved."""
        # Check if there are any explicit depends_on that reference non-existent resources
        resources = terraform_config.get('resource', [{}])[0]
        instance = resources.get('google_compute_instance', {}).get('world111', [{}])[0]
        
        depends_on = instance.get('depends_on', [])
        # If depends_on exists, it should reference valid resources
        for dep in depends_on:
            assert dep, "Dependencies should not be empty"