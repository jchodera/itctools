import unittest
from itctools import materials
from simtk import unit
from mock import Mock


class TestMaterials(unittest.TestCase):

    """Validation of the materials submodule"""

    def _check_solvent(self, args):
        """Validate the structure of a single or two argument Solvent."""
        # [name, density=None]
        defaults = ['', None]
        water = materials.Solvent(*args)
        # Pad the list with defaults to account for missing arguments
        args.extend(defaults[len(args):])
        self.assertListEqual([water.name, water.density], args)

    def test_solvent(self):
        """Ensure Solvent has correct parameter assignment"""
        arguments = [
            ['water'],
            ['water', 0.9970479 * unit.grams / unit.milliliter],
        ]
        for args in arguments:
            self._check_solvent(args)

    def _check_compound(self, args):
        """Validate structure of single, two or three arguments"""
        # [name, molecular_weight=None, purity=1.0]
        defaults = ['', None, 1.00]
        compound = materials.Compound(*args)
        # Pad the list with defaults to account for missing arguments
        args.extend(defaults[len(args):])
        self.assertListEqual(
            [compound.name, compound.molecular_weight, compound.purity, ],
            args)

    def test_compound(self):
        """Ensure Compound has correct parameter assignment"""
        arguments = [['nacl'],
                     ['imatinib mesylate', 589.7 * unit.grams / unit.mole],
                     ['compound1', 209.12 * unit.grams / unit.mole, 0.975]
                     ]

        for args in arguments:
            self._check_compound(args)

    def _check_pureliquid(self, args):
        """Validate the structure of a triple or quadruple argument PureLiquid"""
        # [name, density, molecular_weight, purity=1.0]
        defaults = ['', '', '', 1.0]
        pureliquid = materials.PureLiquid(*args)
        # Pad the list with defaults to account for missing arguments
        args.extend(defaults[len(args):])
        self.assertListEqual([pureliquid.name,
                              pureliquid.density,
                              pureliquid.molecular_weight,
                              pureliquid.purity,
                              ],
                             args)

    def test_pure_liquid(self):
        """Ensure PureLiquid has correct parameter assignment"""
        arguments = [['water', 0.9970479 *
                      unit.grams /
                      unit.milliliter, 18.01528 *
                      unit.gram /
                      unit.mole], ['ethanol', 0.789 *
                                   unit.grams /
                                   unit.milliliter, 46.07 *
                                   unit.gram /
                                   unit.mole, 99.8 /
                                   100.]]
        for args in arguments:
            self._check_pureliquid(args)

    def test_simple_solution(self):
        """Ensure that SimpleSolution has correct parameter assignment"""

        # Using Mock classes to ensure that SimpleSolution works, independently
        # of Compound and Solvent
        mock_compound = Mock(
            name='imatinib',
            molecular_weight=589.7 *
            unit.grams /
            unit.mole,
            purity=1.0)
        compound_mass = 1.0 * unit.milligram
        mock_solvent = Mock(
            name='water', density=0.9970479 * unit.grams / unit.milliliter)
        solvent_mass = 10.0 * unit.grams
        mock_location = Mock(
            RackLabel='DestinationPlate', RackType='ITCPlate', Position=1)

        simple_solution = materials.SimpleSolution(
            mock_compound,
            compound_mass,
            mock_solvent,
            solvent_mass,
            mock_location)

        expected_structure = {
            'solvent': mock_solvent,
            'name': mock_compound.name,
            'compound_mass': compound_mass,
            'density': mock_solvent.density,  # Ideal solution approximation
            'volume': solvent_mass / mock_solvent.density,
            'location': mock_location,
            'compound': mock_compound,
            'solution_mass': compound_mass + solvent_mass,
            'compound_moles': compound_mass / mock_compound.molecular_weight * mock_compound.purity,
            'solvent_mass': solvent_mass,
            'concentration': (compound_mass / mock_compound.molecular_weight * mock_compound.purity) / (solvent_mass / mock_solvent.density),
        }
        self.assertDictEqual(expected_structure, simple_solution.__dict__)

    def test_simple_solution_solvent_compatibility(self):
        """Ensure that SimpleSolution is compatible with Solvent"""

        # Using Mock classes to ensure that SimpleSolution works, independently
        # of Compound
        mock_compound = Mock(
            name='imatinib',
            molecular_weight=589.7 *
            unit.grams /
            unit.mole,
            purity=1.0)
        compound_mass = 1.0 * unit.milligram
        solvent = materials.Solvent(
            'water', density=0.9970479 * unit.grams / unit.milliliter)
        solvent_mass = 10.0 * unit.grams
        mock_location = Mock(
            RackLabel='DestinationPlate', RackType='ITCPlate', Position=1)

        simple_solution = materials.SimpleSolution(
            mock_compound, compound_mass, solvent, solvent_mass, mock_location)

        expected_structure = {
            'solvent': solvent,
            'name': mock_compound.name,
            'compound_mass': compound_mass,
            'density': solvent.density,  # Ideal solution approximation
            'volume': solvent_mass / solvent.density,
            'location': mock_location,
            'compound': mock_compound,
            'solution_mass': compound_mass + solvent_mass,
            'compound_moles': compound_mass / mock_compound.molecular_weight * mock_compound.purity,
            'solvent_mass': solvent_mass,
            'concentration': (compound_mass / mock_compound.molecular_weight * mock_compound.purity) / (solvent_mass / solvent.density),
        }
        self.assertDictEqual(expected_structure, simple_solution.__dict__)

    def test_simple_solution_compound_compatibility(self):
        """Ensure that SimpleSolution is compatible with Compound"""

        # Using Mock classes to ensure that SimpleSolution works, independently
        # of Compound and Solvent
        compound = materials.Compound(
            'imatinib',
            molecular_weight=589.7 *
            unit.grams /
            unit.mole,
            purity=1.0)
        compound_mass = 1.0 * unit.milligram
        mock_solvent = Mock(
            name='water', density=0.9970479 * unit.grams / unit.milliliter)
        solvent_mass = 10.0 * unit.grams
        mock_location = Mock(
            RackLabel='DestinationPlate', RackType='ITCPlate', Position=1)

        simple_solution = materials.SimpleSolution(
            compound, compound_mass, mock_solvent, solvent_mass, mock_location)

        expected_structure = {
            'solvent': mock_solvent,
            'name': compound.name,
            'compound_mass': compound_mass,
            'density': mock_solvent.density,  # Ideal solution approximation
            'volume': solvent_mass / mock_solvent.density,
            'location': mock_location,
            'compound': compound,
            'solution_mass': compound_mass + solvent_mass,
            'compound_moles': compound_mass / compound.molecular_weight * compound.purity,
            'solvent_mass': solvent_mass,
            'concentration': (compound_mass / compound.molecular_weight * compound.purity) / (solvent_mass / mock_solvent.density),
        }

        self.assertDictEqual(expected_structure, simple_solution.__dict__)

    def test_simple_mixture(self):
        """Ensure that SimpleMixture has correct parameter assignment"""
        mock_liquid1 = Mock(
            name='water',
            density=0.9970479 *
            unit.grams /
            unit.milliliter,
            molecular_weight=18.01528 *
            unit.gram /
            unit.mole)
        mock_liquid2 = Mock(
            name='ethanol',
            density=0.789 *
            unit.grams /
            unit.milliliter,
            molecular_weight=46.07 *
            unit.gram /
            unit.mole)
        liquids = [mock_liquid1, mock_liquid2]
        mock_location1 = Mock(
            RackLabel='SourcePlate',
            RackType='5x3 Vial Holder',
            Position=1)
        mock_location2 = Mock(
            RackLabel='SourcePlate',
            RackType='5x3 Vial Holder',
            Position=2)
        locations = [mock_location1, mock_location2]
        fractions = [0.6, 0.4]
        molar_volumes = [liq.molecular_weight / liq.density for liq in liquids]

        normalizing_mass = 0 * unit.grams / unit.mole
        for i, liq in enumerate(liquids):
            normalizing_mass += liq.molecular_weight * fractions[i]

        mass_fractions = [
            fractions[i] *
            liq.molecular_weight /
            normalizing_mass for i,
            liq in enumerate(liquids)]

        normalizing_volume = 0 * unit.liter / unit.mole
        for i, volume in enumerate(molar_volumes):
            normalizing_volume += fractions[i] * volume

        volume_fractions = [
            fractions[i] *
            volume /
            normalizing_volume for i,
            volume in enumerate(molar_volumes)]
        simple_mixture = materials.SimpleMixture(liquids, fractions, locations)

        expected_structure = {
            'components': [mock_liquid1, mock_liquid2],
            'locations': [mock_location1, mock_location2],
            'massfractions': mass_fractions,
            'molefractions': fractions,
            'volumefractions': volume_fractions,
        }
        self.assertDictEqual(expected_structure, simple_mixture.__dict__)
