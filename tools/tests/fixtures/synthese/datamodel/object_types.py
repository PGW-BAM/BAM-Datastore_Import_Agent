"""CREATE object types of the synthesis test project (fictitious, tools/tests/fixtures/synthese/).

Batch = main object (pattern M3: reactants -> synthesis -> batch -> measurements). DLS and TEM use the standard steps.
Instruments are linked by OBJECT fields (pattern M4); the heating stirrer reuses the standard field INSTRUMENT.
"""

from bam_masterdata.datamodel.v0.object_types import ExperimentalStep, Sample
from bam_masterdata.metadata.definitions import ObjectTypeDef, PropertyTypeAssignment


class NanoparticleBatch(Sample):
    defs = ObjectTypeDef(
        code="SAMPLE.NANOPARTICLE_BATCH",
        description="""Batch of nanoparticles from one synthesis//Charge von Nanopartikeln aus einer Synthese""",
        generated_code_prefix="SAM.NPB",
    )

    next_step = PropertyTypeAssignment(
        code="NANO.NEXT_STEP",
        data_type="CONTROLLEDVOCABULARY",
        vocabulary_code="NANO.WORKFLOW_STEP",
        property_label="Next step",
        property_label_de="Nächster Schritt",
        description="""Next workflow step of the batch//Nächster Ablaufschritt der Charge""",
        mandatory=False,
        section="Workflow",
    )

    yield_percent = PropertyTypeAssignment(
        code="NANO.YIELD",
        data_type="REAL",
        property_label="Yield [%]",
        property_label_de="Ausbeute [%]",
        description="""Yield after purification [%]//Ausbeute nach der Aufreinigung [%]""",
        mandatory=False,
        section="Purification",
    )

    centrifuge = PropertyTypeAssignment(
        code="NANO.CENTRIFUGE",
        data_type="OBJECT",
        object_code="INSTRUMENT.CENTRIFUGE",
        property_label="Centrifuge",
        property_label_de="Zentrifuge",
        description="""Centrifuge used for purification (inventory object)//Für die Aufreinigung verwendete Zentrifuge (Inventar-Objekt)""",
        mandatory=False,
        section="Purification",
    )

    target_diameter = PropertyTypeAssignment(
        code="NANO.TARGET_DIAMETER",
        data_type="REAL",
        property_label="Target diameter [nm]",
        property_label_de="Zieldurchmesser [nm]",
        description="""Intended particle diameter [nm]//Angestrebter Partikeldurchmesser [nm]""",
        mandatory=False,
        section="Particle Properties",
    )

    particle_shape = PropertyTypeAssignment(
        code="NANO.PARTICLE_SHAPE",
        data_type="CONTROLLEDVOCABULARY",
        vocabulary_code="NANO.PARTICLE_SHAPE",
        property_label="Particle shape",
        property_label_de="Partikelform",
        description="""Particle shape seen in TEM//Partikelform im TEM""",
        mandatory=False,
        section="Particle Properties",
    )


class NanoparticleSynthesis(ExperimentalStep):
    defs = ObjectTypeDef(
        code="EXPERIMENTAL_STEP.NANOPARTICLE_SYNTHESIS",
        description="""Wet-chemical synthesis of a nanoparticle batch incl. weighing of reactants//Nasschemische Synthese einer Nanopartikel-Charge inkl. Einwaage der Edukte""",
        generated_code_prefix="EXP.NPS",
    )

    mass_silver_nitrate = PropertyTypeAssignment(
        code="NANO.MASS_SILVER_NITRATE",
        data_type="REAL",
        property_label="Mass of silver nitrate [mg]",
        property_label_de="Masse Silbernitrat [mg]",
        description="""Weighed mass of silver nitrate [mg]//Eingewogene Masse Silbernitrat [mg]""",
        mandatory=False,
        section="Weighing Of Reactants",
    )

    mass_sodium_citrate = PropertyTypeAssignment(
        code="NANO.MASS_SODIUM_CITRATE",
        data_type="REAL",
        property_label="Mass of sodium citrate [mg]",
        property_label_de="Masse Natriumcitrat [mg]",
        description="""Weighed mass of trisodium citrate [mg]//Eingewogene Masse Trinatriumcitrat [mg]""",
        mandatory=False,
        section="Weighing Of Reactants",
    )

    balance = PropertyTypeAssignment(
        code="NANO.BALANCE",
        data_type="OBJECT",
        object_code="INSTRUMENT.SCALE",
        property_label="Balance",
        property_label_de="Waage",
        description="""Balance used for weighing (inventory object)//Für die Einwaage verwendete Waage (Inventar-Objekt)""",
        mandatory=False,
        section="Weighing Of Reactants",
    )

    reaction_temperature = PropertyTypeAssignment(
        code="NANO.REACTION_TEMPERATURE",
        data_type="REAL",
        property_label="Reaction temperature [°C]",
        property_label_de="Reaktionstemperatur [°C]",
        description="""Reaction temperature [°C]//Reaktionstemperatur [°C]""",
        mandatory=False,
        section="Synthesis Conditions",
    )

    reaction_time = PropertyTypeAssignment(
        code="NANO.REACTION_TIME",
        data_type="REAL",
        property_label="Reaction time [min]",
        property_label_de="Reaktionszeit [min]",
        description="""Reaction time [min]//Reaktionszeit [min]""",
        mandatory=True,
        section="Synthesis Conditions",
    )

    instrument = PropertyTypeAssignment(
        code="INSTRUMENT",
        data_type="OBJECT",  # any target, like "(ALL)" in the standard; the checker accepts only an empty object_code
        property_label="Testing Machine or Measurement Device",
        description="""Testing machine or measurement device//Prüfmaschine oder Messgerät""",
        mandatory=False,
        section="Synthesis Conditions",
    )
