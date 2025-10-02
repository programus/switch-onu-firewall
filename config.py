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


onu = OnuSetting()
webui = WebUISetting()