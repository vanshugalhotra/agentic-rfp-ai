def applicable_tests_for_product(product: dict, test_catalog: list) -> list:
    voltage = product.get("voltage_rating", 0)

    applicable_tests = []

    for test in test_catalog:
        rule = test["applicable_to"]

        if rule == "All Cables":
            applicable_tests.append(test)

        elif rule == ">11kV Cables" and voltage > 11:
            applicable_tests.append(test)

        elif rule == "LV Cables" and voltage <= 1.1:
            applicable_tests.append(test)

        elif rule == "MV Cables" and 11 < voltage <= 33:
            applicable_tests.append(test)

    return applicable_tests
