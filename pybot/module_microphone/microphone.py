from speech_recognition import Microphone as SrMicrophone, Recognizer, AudioData

import logging
from datetime import datetime

from typing import Callable
from .traitement_audio import TraitementAudio
from .utils import textual_duration_to_seconds


_debug = logging.getLogger("Microphone").debug
_error = logging.getLogger("Microphone").error

"""Custom Logger debug function. Print a message only shown when DEBUG mode is activated."""


def _get_default_recognizer() -> Recognizer:
    """
    Get a configured recognizer that should be able to recognize voice in a loud environment. `Energy_threshold` will adjust itself over time.
    """
    r = Recognizer()
    r.energy_threshold = 4000
    return r


class Microphone:
    """
    Permet d'enregistrer l'audio de différentes manières. Les méthodes sont châinables pour ensuite pour effectuer des traitements sur le fichier audio comme l'enregistrer dans un fichier, ou le transcrire.
    """

    is_recording: bool = False

    def __init__(self, recognizer: Recognizer = _get_default_recognizer()) -> None:
        self.r = recognizer
        self.mic = SrMicrophone()

    def pour_chaque_phrase(self, callback: Callable[[TraitementAudio], None]):
        """
        Enregistre chaque phrase parlée. Dès qu'une phrase est terminée, la fonction donnée en paramètre est appellée. Cette méthode n'est pas bloquante.
        Au début de l'enregistrement, il faut attendre quelque secondes sans parler, le microphone s'ajuste au bruit ambiant pour être ensuite capable de détecter les silences.
        """

        def cb(r: Recognizer, recording: AudioData):
            return callback(TraitementAudio(recording, recognizer=r))

        _debug(
            "Je m'ajuste au bruit ambiant pour pouvoir détecter les silences, celà prend quelques secondes..."
        )

        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)

        _debug("J'écoute la parole en arrière plan...")

        # TODO add attribute is_recording for when recording is running
        self.stop = self.r.listen_in_background(self.mic, cb)
        return self.stop

    def une_phrase(self) -> "TraitementAudio":
        """
        Enregistre uniquement une phrase. L'enregistrement commence quand cette méthode est appellée, et s'arrête quand la personne arrête de parler pendant plus d'une seconde.

        Retour:
            TraitementAudio: L'enregistrement prêt à être manipulé.
        """
        with SrMicrophone() as source:
            _debug("Écoute d'une phrase")
            start_time = datetime.now()
            self.r.pause_threshold = 1
            recording = self.r.listen(source)
            _debug("Écoute terminée...")
            return TraitementAudio(recording, start_time=start_time, recognizer=self.r)

    def pendant(
        self, duree: str | float, delai: str | float | None = None
    ) -> "TraitementAudio":
        """
        Enregistre l'audio pendant la durée specifiée, avec un délai optionel. Le délai, permet d'attendre un certain temps avant que l'enregistrement ne commence.
        La durée et le délai peuvent être données soit en secondes (exemple: 5), soit en toutes lettres (exemple: "1 minute et 30 secondes").

        Paramètres:
            duree (str|float): Soit un nombre qui représente la durée de l'enregistrement en secondes, soit une durée en toutes lettres comme "1 minute et 30 secondes".
            decalage (float): Un délai avant que l'enregistrement ne commence.

        Retour:
            TraitementAudio: L'enregistrement prêt à être manipulé.
        """
        if isinstance(duree, str):
            try:
                duree = textual_duration_to_seconds(duree)
            except ValueError as e:
                _error(
                    f'L\'enregistrement n\'a pas pu commencer. Erreur dans la fonction "pendant", argument "duree" invalide: {e}',
                )  # TODO humanize date
                return TraitementAudio()

        if isinstance(delai, str):
            try:
                delai = textual_duration_to_seconds(delai)
            except ValueError as e:
                _error(
                    f'L\'enregistrement n\'a pas pu commencer. Erreur dans la fonction "pendant", argument "delai" invalide: {e}',
                )  # TODO humanize date
                return TraitementAudio()

        with SrMicrophone() as source:
            _debug(f"J'écoute pendant {duree} secondes...")  # TODO humanize date
            start_time = datetime.now()
            recording = self.r.record(source, duration=duree, offset=delai)
            _debug("Écoute terminée...")
            return TraitementAudio(recording, start_time=start_time, recognizer=self.r)


ecoute = Microphone()
"""Un microphone prêt à être utilisé."""
