package com.radiohelper.dosecalc

object DoseCoefficients {
    val values: Map<Region, Map<AgeGroup, Double>> = mapOf(
        Region.HEAD to mapOf(
            AgeGroup.GT_15 to 0.0023,
            AgeGroup.Y15 to 0.00276,
            AgeGroup.Y10 to 0.0046,
            AgeGroup.Y5 to 0.00736,
            AgeGroup.Y1 to 0.01173,
            AgeGroup.Y0_1 to 0.02185,
        ),
        Region.BODY to mapOf(
            AgeGroup.GT_15 to 0.0081,
            AgeGroup.Y15 to 0.00972,
            AgeGroup.Y10 to 0.01458,
            AgeGroup.Y5 to 0.02106,
            AgeGroup.Y1 to 0.03240,
            AgeGroup.Y0_1 to 0.06399,
        )
    )
}
