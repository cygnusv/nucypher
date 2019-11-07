import functools
import json

import click
from constant_sorrow.constants import NO_BLOCKCHAIN_CONNECTION

from nucypher.characters.banners import ALICE_BANNER
from nucypher.cli import actions, painting, types
from nucypher.cli.actions import get_nucypher_password, select_client_account, get_client_password
from nucypher.cli.common_options import *
from nucypher.cli.config import group_general_config
from nucypher.cli.types import NETWORK_PORT, EXISTING_READABLE_FILE, EIP55_CHECKSUM_ADDRESS
from nucypher.config.characters import AliceConfiguration
from nucypher.config.keyring import NucypherKeyring
from nucypher.utilities.sandbox.constants import TEMPORARY_DOMAIN


option_bob_verifying_key = click.option(
    '--bob-verifying-key', help="Bob's verifying key as a hexadecimal string", type=click.STRING,
    required=True)
option_pay_with = click.option(
    '--pay-with', help="Run with a specified account", type=EIP55_CHECKSUM_ADDRESS)


class AliceConfigOptions:

    __option_name__ = 'config_options'

    def __init__(
            self, dev, network, provider_uri, geth, federated_only, discovery_port,
            pay_with, registry_filepath, middleware):

        if federated_only and geth:
            raise click.BadOptionUsage(
                option_name="--geth",
                message="--federated-only cannot be used with the --geth flag")

        # Managed Ethereum Client
        eth_node = NO_BLOCKCHAIN_CONNECTION
        if geth:
            eth_node = actions.get_provider_process()
            provider_uri = ETH_NODE.provider_uri(scheme='file')

        self.dev = dev
        self.domains = {network} if network else None
        self.provider_uri = provider_uri
        self.geth = geth
        self.federated_only = federated_only
        self.eth_node = eth_node
        self.pay_with = pay_with
        self.discovery_port = discovery_port
        self.registry_filepath = registry_filepath
        self.middleware = middleware

    def create_config(self, emitter, config_file):

        if self.dev:
            return AliceConfiguration(
                emitter=emitter,
                dev_mode=True,
                network_middleware=self.middleware,
                domains={TEMPORARY_DOMAIN},
                provider_process=self.eth_node,
                provider_uri=self.provider_uri,
                federated_only=True) # FIXME: add error if --federated-only is not True?

        else:
            try:
                return AliceConfiguration.from_configuration_file(
                    emitter=emitter,
                    dev_mode=False,
                    network_middleware=self.middleware,
                    domains=self.domains,
                    provider_process=self.eth_node,
                    provider_uri=self.provider_uri,
                    filepath=config_file,
                    rest_port=self.discovery_port,
                    checksum_address=self.pay_with,
                    registry_filepath=self.registry_filepath)
            except FileNotFoundError:
                return actions.handle_missing_configuration_file(
                    character_config_class=AliceConfiguration,
                    config_file=config_file)

    def generate_config(self, emitter, config_root, poa, light, m, n, duration_periods, rate):

        if self.dev:
            raise click.BadArgumentUsage("Cannot create a persistent development character")

        if not self.provider_uri and not self.federated_only:
            raise click.BadOptionUsage(
                option_name='--provider',
                message="--provider is required to create a new decentralized alice.")

        pay_with = self.pay_with
        if not pay_with and not self.federated_only:
            pay_with = select_client_account(
                emitter=emitter,
                provider_uri=self.provider_uri)

        return AliceConfiguration.generate(
            password=get_nucypher_password(confirm=True),
            config_root=config_root, # FIXME: or DEFAULT_CONFIG_ROOT?
            checksum_address=pay_with,
            domains=self.domains,
            federated_only=self.federated_only,
            provider_uri=self.provider_uri,
            provider_process=self.eth_node,
            registry_filepath=self.registry_filepath,
            poa=poa,
            light=light,
            m=m,
            n=n,
            duration_periods=duration_periods,
            rate=rate)


group_config_options = group_options(
    AliceConfigOptions,
    dev=option_dev,
    network=option_network,
    provider_uri=option_provider_uri(),
    geth=option_geth,
    federated_only=option_federated_only,
    discovery_port=option_discovery_port(),
    pay_with=option_pay_with,
    registry_filepath=option_registry_filepath,
    middleware=option_middleware,
    )


class AliceCharacterOptions:

    __option_name__ = 'character_options'

    def __init__(self, config_options, hw_wallet, teacher_uri, min_stake):
        self.config_options = config_options
        self.hw_wallet = hw_wallet
        self.teacher_uri = teacher_uri
        self.min_stake = min_stake

    def create_character(self, emitter, config_file, json_ipc, load_seednodes=True):

        config = self.config_options.create_config(emitter, config_file)

        client_password = None
        if not config.federated_only:
            if (not self.hw_wallet or not config.dev_mode) and not json_ipc:
                client_password = get_client_password(checksum_address=config.checksum_address)

        try:
            ALICE = actions.make_cli_character(character_config=config,
                                               emitter=emitter,
                                               unlock_keyring=not config.dev_mode,
                                               teacher_uri=self.teacher_uri,
                                               min_stake=self.min_stake,
                                               client_password=client_password,
                                               load_preferred_teachers=load_seednodes,
                                               start_learning_now=load_seednodes)

            return ALICE
        except NucypherKeyring.AuthenticationFailed as e:
            emitter.echo(str(e), color='red', bold=True)
            click.get_current_context().exit(1)


group_character_options = group_options(
    AliceCharacterOptions,
    config_options=group_config_options,
    hw_wallet=option_hw_wallet,
    teacher_uri=option_teacher_uri,
    min_stake=option_min_stake,
    )


@click.group()
def alice():
    """
    "Alice the Policy Authority" management commands.
    """
    pass


@alice.command()
@group_config_options
@option_config_root
@option_poa
@option_light
@option_m
@option_n
@click.option('--rate', help="Policy rate per period in wei", type=click.FLOAT)
@click.option('--duration-periods', help="Policy duration in periods", type=click.FLOAT)
@group_general_config
def init(general_config, config_options, config_root, poa, light, m, n, rate, duration_periods):
    """
    Create a brand new persistent Alice.
    """

    emitter = _setup_emitter(general_config)

    if not config_root:
        config_root = general_config.config_file # FIXME: better called `config_root`?

    new_alice_config = config_options.generate_config(
        emitter, config_root, poa, light, m, n, duration_periods, rate)

    painting.paint_new_installation_help(emitter, new_configuration=new_alice_config)


@alice.command()
@option_config_file
@group_general_config
def view(general_config, config_file):
    """
    View existing Alice's configuration.
    """
    emitter = _setup_emitter(general_config)
    configuration_file_location = config_file or AliceConfiguration.default_filepath()
    response = AliceConfiguration._read_configuration_file(filepath=configuration_file_location)
    emitter.echo(f"Alice Configuration {configuration_file_location} \n {'='*55}")
    return emitter.echo(json.dumps(response, indent=4))


@alice.command()
@group_config_options
@option_config_file
@option_force
@group_general_config
def destroy(general_config, config_options, config_file, force):
    """
    Delete existing Alice's configuration.
    """
    emitter = _setup_emitter(general_config)
    alice_config = config_options.create_config(emitter, config_file)
    return actions.destroy_configuration(emitter, character_config=alice_config, force=force)


@alice.command()
@group_character_options
@option_config_file
@option_controller_port(default=AliceConfiguration.DEFAULT_CONTROLLER_PORT)
@option_dry_run
@group_general_config
def run(general_config, character_options, config_file, controller_port, dry_run):
    """
    Start Alice's controller.
    """
    emitter = _setup_emitter(general_config)
    ALICE = character_options.create_character(
        emitter, config_file, general_config.json_ipc)

    try:
        # RPC
        if general_config.json_ipc:
            rpc_controller = ALICE.make_rpc_controller()
            _transport = rpc_controller.make_control_transport()
            rpc_controller.start()
            return

        # HTTP
        else:
            emitter.message(f"Alice Verifying Key {bytes(ALICE.stamp).hex()}", color="green", bold=True)
            controller = ALICE.make_web_controller(crash_on_error=general_config.debug)
            ALICE.log.info('Starting HTTP Character Web Controller')
            emitter.message(f'Running HTTP Alice Controller at http://localhost:{controller_port}')
            return controller.start(http_port=controller_port, dry_run=dry_run)

    # Handle Crash
    except Exception as e:
        ALICE.log.critical(str(e))
        emitter.message(f"{e.__class__.__name__} {e}", color='red', bold=True)
        if general_config.debug:
            raise  # Crash :-(


@alice.command("public-keys")
@group_character_options
@option_config_file
@group_general_config
def public_keys(general_config, character_options, config_file):
    """
    Obtain Alice's public verification and encryption keys.
    """
    emitter = _setup_emitter(general_config)
    ALICE = character_options.create_character(emitter, config_file, general_config.json_ipc, load_seednodes=False)
    response = ALICE.controller.public_keys()
    return response


@alice.command('derive-policy-pubkey')
@option_label(required=True)
@group_character_options
@option_config_file
@group_general_config
def derive_policy_pubkey(general_config, label, character_options, config_file):
    """
    Get a policy public key from a policy label.
    """
    ### Setup ###
    emitter = _setup_emitter(general_config)
    ALICE = character_options.create_character(emitter, config_file, general_config.json_ipc, load_seednodes=False)
    return ALICE.controller.derive_policy_encrypting_key(label=label)


@alice.command()
@click.option('--bob-encrypting-key', help="Bob's encrypting key as a hexadecimal string", type=click.STRING,
              required=True)
@option_bob_verifying_key
@option_label(required=True)
@option_m
@option_n
@click.option('--expiration', help="Expiration Datetime of a policy", type=click.STRING)  # TODO: click.DateTime()
@click.option('--value', help="Total policy value (in Wei)", type=types.WEI)
@group_character_options
@option_config_file
@group_general_config
def grant(general_config,
          # Other (required)
          bob_encrypting_key, bob_verifying_key, label,

          # Other
          m, n, expiration, value,

          # API Options
          character_options, config_file
          ):
    """
    Create and enact an access policy for some Bob.
    """
    ### Setup ###
    emitter = _setup_emitter(general_config)

    ALICE = character_options.create_character(emitter, config_file, general_config.json_ipc)

    # Request
    grant_request = {
        'bob_encrypting_key': bob_encrypting_key,
        'bob_verifying_key': bob_verifying_key,
        'label': label,
        'm': m,
        'n': n,
        'expiration': expiration,
    }

    if not ALICE.federated_only:
        grant_request.update({'value': value})
    return ALICE.controller.grant(request=grant_request)


@alice.command()
@option_bob_verifying_key
@option_label(required=True)
@group_character_options
@option_config_file
@group_general_config
def revoke(general_config,

           # Other (required)
           bob_verifying_key, label,

           # API Options
           character_options, config_file
           ):
    """
    Revoke a policy.
    """
    ### Setup ###
    emitter = _setup_emitter(general_config)

    ALICE = character_options.create_character(emitter, config_file, general_config.json_ipc)

    # Request
    revoke_request = {'label': label, 'bob_verifying_key': bob_verifying_key}
    return ALICE.controller.revoke(request=revoke_request)


@alice.command()
@option_label(required=True)
@option_message_kit(required=True)
@group_character_options
@option_config_file
@group_general_config
def decrypt(general_config,

            # Other (required)
            label, message_kit,

            # API Options
            character_options, config_file
            ):
    """
    Decrypt data encrypted under an Alice's policy public key.
    """
    ### Setup ###
    emitter = _setup_emitter(general_config)

    ALICE = character_options.create_character(emitter, config_file, general_config.json_ipc, load_seednodes=False)

    # Request
    request_data = {'label': label, 'message_kit': message_kit}
    response = ALICE.controller.decrypt(request=request_data)
    return response


def _setup_emitter(general_config):
    # Banner
    emitter = general_config.emitter
    emitter.clear()
    emitter.banner(ALICE_BANNER)

    return emitter
