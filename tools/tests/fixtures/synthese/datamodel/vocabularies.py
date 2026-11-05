"""CREATE vocabularies of the synthesis test project (fictitious)."""

from bam_masterdata.metadata.definitions import VocabularyTerm, VocabularyTypeDef
from bam_masterdata.metadata.entities import VocabularyType


class NanoParticleShape(VocabularyType):
    defs = VocabularyTypeDef(
        code="NANO.PARTICLE_SHAPE",
        description="""Shape of nanoparticles//Form von Nanopartikeln""",
    )

    sphere = VocabularyTerm(code="SPHERE", label="Sphere", label_de="Kugel", description="""Spherical particles//Kugelförmige Partikel""")
    rod = VocabularyTerm(code="ROD", label="Rod", label_de="Stäbchen", description="""Rod-shaped particles//Stäbchenförmige Partikel""")
    plate = VocabularyTerm(code="PLATE", label="Plate", label_de="Plättchen", description="""Plate-shaped particles//Plättchenförmige Partikel""")


class NanoWorkflowStep(VocabularyType):
    defs = VocabularyTypeDef(
        code="NANO.WORKFLOW_STEP",
        description="""Ordered workflow steps of the nanoparticle synthesis//Geordnete Ablaufschritte der Nanopartikel-Synthese""",
    )

    s01 = VocabularyTerm(code="S01_WEIGHING", label="01 Weighing of reactants", label_de="01 Einwaage der Edukte", description="""Weighing of reactants//Einwaage der Edukte""")
    s02 = VocabularyTerm(code="S02_SYNTHESIS", label="02 Synthesis", label_de="02 Synthese", description="""Synthesis//Synthese""")
    s03 = VocabularyTerm(code="S03_PURIFICATION", label="03 Purification", label_de="03 Aufreinigung", description="""Purification//Aufreinigung""")
    s04 = VocabularyTerm(code="S04_DLS", label="04 DLS measurement", label_de="04 DLS-Messung", description="""DLS measurement//DLS-Messung""")
    s05 = VocabularyTerm(code="S05_TEM", label="05 TEM imaging", label_de="05 TEM-Aufnahmen", description="""TEM imaging//TEM-Aufnahmen""")
    done = VocabularyTerm(code="DONE", label="Done", label_de="Abgeschlossen", description="""All steps done//Alle Schritte abgeschlossen""")
