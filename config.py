from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class OnuSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_prefix='ONU_', extra='ignore')

    host: str = '192.168.1.1'
    username: str = 'admin'
    password: str = 'password'


class WebUISetting(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', env_prefix='LISTEN_', extra='ignore')

    host: str = '0.0.0.0'
    port: int = 8080


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore', env_prefix='APP_')

    username: str = 'admin'
    password: str = 'Passw0rd!'
    storage_secret: str = 'change_this_to_a_random_secret'


onu = OnuSetting()
webui = WebUISetting()
app = AppSettings()