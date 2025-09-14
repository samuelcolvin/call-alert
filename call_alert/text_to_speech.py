import random
from dataclasses import dataclass
from tempfile import NamedTemporaryFile
from typing import Literal

import httpx
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2.service_account import Credentials
from playsound import playsound  # type: ignore
from pydantic import Base64Bytes, BaseModel, Field

google_auth_scopes = ['https://www.googleapis.com/auth/cloud-platform']


def play_text(text: str):
    auth_token = get_auth_token()

    # voice = random.choice(english_voices)
    # print('voice chosen:', random_voice)
    voice = Voice(name='en-GB-Chirp3-HD-Zephyr', language_code='en-GB')

    request_data = {
        'audioConfig': {
            'audioEncoding': 'LINEAR16',
            # https://cloud.google.com/text-to-speech/docs/audio-profiles
            'effectsProfileId': ['large-home-entertainment-class-device'],
            'pitch': 0,
            'speakingRate': 1,
        },
        'input': {'text': text},
        'voice': {'languageCode': voice.language_code, 'name': voice.name},
    }
    r = httpx.post(
        'https://texttospeech.googleapis.com/v1beta1/text:synthesize',
        json=request_data,
        headers={'Authorization': f'Bearer {auth_token}'},
    )
    if r.status_code != 200:
        raise ValueError(f'Error synthesising text: {r.status_code}, body:\n{r.text}')

    class AudioResponse(BaseModel):
        audio_content: Base64Bytes = Field(validation_alias='audioContent')

    response = AudioResponse.model_validate_json(r.content)

    with NamedTemporaryFile() as fp:
        fp.write(response.audio_content)
        fp.flush()
        fp.seek(0)
        playsound(fp.name)


def get_voices():
    auth_token = get_auth_token()

    r = httpx.get(
        'https://texttospeech.googleapis.com/v1beta1/voices',
        headers={'Authorization': f'Bearer {auth_token}'},
    )
    if r.status_code != 200:
        raise ValueError(f'Error getting voices: {r.status_code}, body:\n{r.text}')

    class VoiceInfo(BaseModel):
        language_codes: list[str] = Field(validation_alias='languageCodes')
        name: str
        ssml_gender: Literal['MALE', 'FEMALE'] = Field(validation_alias='ssmlGender')
        natural_sample_rate_hertz: int = Field(validation_alias='naturalSampleRateHertz')

        @property
        def language_code(self) -> str:
            assert len(self.language_codes) == 1
            return self.language_codes[0]

    class VoiceResponse(BaseModel):
        voices: list[VoiceInfo]

    voice_response = VoiceResponse.model_validate_json(r.content)
    english_voices = [voice for voice in voice_response.voices if voice.language_code.startswith('en')]
    print(english_voices)
    # TODO save these to file


def get_auth_token() -> str:
    credentials = Credentials.from_service_account_file(  # type: ignore[reportUnknownMemberType]
        'service-account.json', scopes=google_auth_scopes
    )
    if credentials.token is None:  # type: ignore[reportUnknownMemberType]
        credentials.refresh(GoogleAuthRequest())  # type: ignore[reportUnknownMemberType]
    return credentials.token  # type: ignore[reportUnknownMemberType]


@dataclass
class Voice:
    name: str
    language_code: str


english_voices = [
    Voice(name='Achernar', language_code='en-US'),
    Voice(name='Achird', language_code='en-US'),
    Voice(name='Algenib', language_code='en-US'),
    Voice(name='Algieba', language_code='en-US'),
    Voice(name='Alnilam', language_code='en-US'),
    Voice(name='Aoede', language_code='en-US'),
    Voice(name='Autonoe', language_code='en-US'),
    Voice(name='Callirrhoe', language_code='en-US'),
    Voice(name='Charon', language_code='en-US'),
    Voice(name='Despina', language_code='en-US'),
    Voice(name='Enceladus', language_code='en-US'),
    Voice(name='Erinome', language_code='en-US'),
    Voice(name='Fenrir', language_code='en-US'),
    Voice(name='Gacrux', language_code='en-US'),
    Voice(name='Iapetus', language_code='en-US'),
    Voice(name='Kore', language_code='en-US'),
    Voice(name='Laomedeia', language_code='en-US'),
    Voice(name='Leda', language_code='en-US'),
    Voice(name='Orus', language_code='en-US'),
    Voice(name='Puck', language_code='en-US'),
    Voice(name='Pulcherrima', language_code='en-US'),
    Voice(name='Rasalgethi', language_code='en-US'),
    Voice(name='Sadachbia', language_code='en-US'),
    Voice(name='Sadaltager', language_code='en-US'),
    Voice(name='Schedar', language_code='en-US'),
    Voice(name='Sulafat', language_code='en-US'),
    Voice(name='Umbriel', language_code='en-US'),
    Voice(name='Vindemiatrix', language_code='en-US'),
    Voice(name='Zephyr', language_code='en-US'),
    Voice(name='Zubenelgenubi', language_code='en-US'),
    Voice(name='en-AU-Chirp-HD-D', language_code='en-AU'),
    Voice(name='en-AU-Chirp-HD-F', language_code='en-AU'),
    Voice(name='en-AU-Chirp-HD-O', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Achernar', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Achird', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Algenib', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Algieba', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Alnilam', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Aoede', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Autonoe', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Callirrhoe', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Charon', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Despina', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Enceladus', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Erinome', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Fenrir', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Gacrux', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Iapetus', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Kore', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Laomedeia', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Leda', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Orus', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Puck', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Pulcherrima', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Rasalgethi', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Sadachbia', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Sadaltager', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Schedar', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Sulafat', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Umbriel', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Vindemiatrix', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Zephyr', language_code='en-AU'),
    Voice(name='en-AU-Chirp3-HD-Zubenelgenubi', language_code='en-AU'),
    Voice(name='en-AU-Neural2-A', language_code='en-AU'),
    Voice(name='en-AU-Neural2-B', language_code='en-AU'),
    Voice(name='en-AU-Neural2-C', language_code='en-AU'),
    Voice(name='en-AU-Neural2-D', language_code='en-AU'),
    Voice(name='en-AU-News-E', language_code='en-AU'),
    Voice(name='en-AU-News-F', language_code='en-AU'),
    Voice(name='en-AU-News-G', language_code='en-AU'),
    Voice(name='en-AU-Polyglot-1', language_code='en-AU'),
    Voice(name='en-AU-Standard-A', language_code='en-AU'),
    Voice(name='en-AU-Standard-B', language_code='en-AU'),
    Voice(name='en-AU-Standard-C', language_code='en-AU'),
    Voice(name='en-AU-Standard-D', language_code='en-AU'),
    Voice(name='en-AU-Wavenet-A', language_code='en-AU'),
    Voice(name='en-AU-Wavenet-B', language_code='en-AU'),
    Voice(name='en-AU-Wavenet-C', language_code='en-AU'),
    Voice(name='en-AU-Wavenet-D', language_code='en-AU'),
    Voice(name='en-GB-Chirp-HD-D', language_code='en-GB'),
    Voice(name='en-GB-Chirp-HD-F', language_code='en-GB'),
    Voice(name='en-GB-Chirp-HD-O', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Achernar', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Achird', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Algenib', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Algieba', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Alnilam', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Aoede', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Autonoe', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Callirrhoe', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Charon', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Despina', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Enceladus', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Erinome', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Fenrir', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Gacrux', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Iapetus', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Kore', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Laomedeia', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Leda', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Orus', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Puck', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Pulcherrima', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Rasalgethi', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Sadachbia', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Sadaltager', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Schedar', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Sulafat', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Umbriel', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Vindemiatrix', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Zephyr', language_code='en-GB'),
    Voice(name='en-GB-Chirp3-HD-Zubenelgenubi', language_code='en-GB'),
    Voice(name='en-GB-Neural2-A', language_code='en-GB'),
    Voice(name='en-GB-Neural2-B', language_code='en-GB'),
    Voice(name='en-GB-Neural2-C', language_code='en-GB'),
    Voice(name='en-GB-Neural2-D', language_code='en-GB'),
    Voice(name='en-GB-Neural2-F', language_code='en-GB'),
    Voice(name='en-GB-Neural2-N', language_code='en-GB'),
    Voice(name='en-GB-Neural2-O', language_code='en-GB'),
    Voice(name='en-GB-News-G', language_code='en-GB'),
    Voice(name='en-GB-News-H', language_code='en-GB'),
    Voice(name='en-GB-News-I', language_code='en-GB'),
    Voice(name='en-GB-News-J', language_code='en-GB'),
    Voice(name='en-GB-News-K', language_code='en-GB'),
    Voice(name='en-GB-News-L', language_code='en-GB'),
    Voice(name='en-GB-News-M', language_code='en-GB'),
    Voice(name='en-GB-Standard-A', language_code='en-GB'),
    Voice(name='en-GB-Standard-B', language_code='en-GB'),
    Voice(name='en-GB-Standard-C', language_code='en-GB'),
    Voice(name='en-GB-Standard-D', language_code='en-GB'),
    Voice(name='en-GB-Standard-F', language_code='en-GB'),
    Voice(name='en-GB-Standard-N', language_code='en-GB'),
    Voice(name='en-GB-Standard-O', language_code='en-GB'),
    Voice(name='en-GB-Studio-B', language_code='en-GB'),
    Voice(name='en-GB-Studio-C', language_code='en-GB'),
    Voice(name='en-GB-Wavenet-A', language_code='en-GB'),
    Voice(name='en-GB-Wavenet-B', language_code='en-GB'),
    Voice(name='en-GB-Wavenet-C', language_code='en-GB'),
    Voice(name='en-GB-Wavenet-D', language_code='en-GB'),
    Voice(name='en-GB-Wavenet-F', language_code='en-GB'),
    Voice(name='en-GB-Wavenet-N', language_code='en-GB'),
    Voice(name='en-GB-Wavenet-O', language_code='en-GB'),
    Voice(name='en-IN-Chirp-HD-D', language_code='en-IN'),
    Voice(name='en-IN-Chirp-HD-F', language_code='en-IN'),
    Voice(name='en-IN-Chirp-HD-O', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Achernar', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Achird', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Algenib', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Algieba', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Alnilam', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Aoede', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Autonoe', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Callirrhoe', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Charon', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Despina', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Enceladus', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Erinome', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Fenrir', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Gacrux', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Iapetus', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Kore', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Laomedeia', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Leda', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Orus', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Puck', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Pulcherrima', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Rasalgethi', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Sadachbia', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Sadaltager', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Schedar', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Sulafat', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Umbriel', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Vindemiatrix', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Zephyr', language_code='en-IN'),
    Voice(name='en-IN-Chirp3-HD-Zubenelgenubi', language_code='en-IN'),
    Voice(name='en-IN-Neural2-A', language_code='en-IN'),
    Voice(name='en-IN-Neural2-B', language_code='en-IN'),
    Voice(name='en-IN-Neural2-C', language_code='en-IN'),
    Voice(name='en-IN-Neural2-D', language_code='en-IN'),
    Voice(name='en-IN-Standard-A', language_code='en-IN'),
    Voice(name='en-IN-Standard-B', language_code='en-IN'),
    Voice(name='en-IN-Standard-C', language_code='en-IN'),
    Voice(name='en-IN-Standard-D', language_code='en-IN'),
    Voice(name='en-IN-Standard-E', language_code='en-IN'),
    Voice(name='en-IN-Standard-F', language_code='en-IN'),
    Voice(name='en-IN-Wavenet-A', language_code='en-IN'),
    Voice(name='en-IN-Wavenet-B', language_code='en-IN'),
    Voice(name='en-IN-Wavenet-C', language_code='en-IN'),
    Voice(name='en-IN-Wavenet-D', language_code='en-IN'),
    Voice(name='en-IN-Wavenet-E', language_code='en-IN'),
    Voice(name='en-IN-Wavenet-F', language_code='en-IN'),
    Voice(name='en-US-Casual-K', language_code='en-US'),
    Voice(name='en-US-Chirp-HD-D', language_code='en-US'),
    Voice(name='en-US-Chirp-HD-F', language_code='en-US'),
    Voice(name='en-US-Chirp-HD-O', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Achernar', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Achird', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Algenib', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Algieba', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Alnilam', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Aoede', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Autonoe', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Callirrhoe', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Charon', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Despina', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Enceladus', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Erinome', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Fenrir', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Gacrux', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Iapetus', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Kore', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Laomedeia', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Leda', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Orus', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Puck', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Pulcherrima', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Rasalgethi', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Sadachbia', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Sadaltager', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Schedar', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Sulafat', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Umbriel', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Vindemiatrix', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Zephyr', language_code='en-US'),
    Voice(name='en-US-Chirp3-HD-Zubenelgenubi', language_code='en-US'),
    Voice(name='en-US-Neural2-A', language_code='en-US'),
    Voice(name='en-US-Neural2-C', language_code='en-US'),
    Voice(name='en-US-Neural2-D', language_code='en-US'),
    Voice(name='en-US-Neural2-E', language_code='en-US'),
    Voice(name='en-US-Neural2-F', language_code='en-US'),
    Voice(name='en-US-Neural2-G', language_code='en-US'),
    Voice(name='en-US-Neural2-H', language_code='en-US'),
    Voice(name='en-US-Neural2-I', language_code='en-US'),
    Voice(name='en-US-Neural2-J', language_code='en-US'),
    Voice(name='en-US-News-K', language_code='en-US'),
    Voice(name='en-US-News-L', language_code='en-US'),
    Voice(name='en-US-News-N', language_code='en-US'),
    Voice(name='en-US-Polyglot-1', language_code='en-US'),
    Voice(name='en-US-Standard-A', language_code='en-US'),
    Voice(name='en-US-Standard-B', language_code='en-US'),
    Voice(name='en-US-Standard-C', language_code='en-US'),
    Voice(name='en-US-Standard-D', language_code='en-US'),
    Voice(name='en-US-Standard-E', language_code='en-US'),
    Voice(name='en-US-Standard-F', language_code='en-US'),
    Voice(name='en-US-Standard-G', language_code='en-US'),
    Voice(name='en-US-Standard-H', language_code='en-US'),
    Voice(name='en-US-Standard-I', language_code='en-US'),
    Voice(name='en-US-Standard-J', language_code='en-US'),
    Voice(name='en-US-Studio-O', language_code='en-US'),
    Voice(name='en-US-Studio-Q', language_code='en-US'),
    Voice(name='en-US-Wavenet-A', language_code='en-US'),
    Voice(name='en-US-Wavenet-B', language_code='en-US'),
    Voice(name='en-US-Wavenet-C', language_code='en-US'),
    Voice(name='en-US-Wavenet-D', language_code='en-US'),
    Voice(name='en-US-Wavenet-E', language_code='en-US'),
    Voice(name='en-US-Wavenet-F', language_code='en-US'),
    Voice(name='en-US-Wavenet-G', language_code='en-US'),
    Voice(name='en-US-Wavenet-H', language_code='en-US'),
    Voice(name='en-US-Wavenet-I', language_code='en-US'),
    Voice(name='en-US-Wavenet-J', language_code='en-US'),
]
