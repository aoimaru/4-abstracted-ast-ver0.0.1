

### 構造化データの構造について


```bash
 {
        "children": [
            {
                "children": [
                    {
                        "children": [
                            {
                                "children": [],
                                "type": "SC-SET-F-E"
                            },
                            {
                                "children": [],
                                "type": "SC-SET-F-U"
                            },
                            {
                                "children": [],
                                "type": "SC-SET-F-X"
                            }
                        ],
                        "type": "SC-SET"
                    },
                    {
                        "children": [],
                        "type": "SC-APT-GET-UPDATE"
                    },
                    {
                        "children": [
                            {
                                "children": [],
                                "type": "SC-APT-GET-F-YES"
                            },
                            {
                                "children": [],
                                "type": "SC-APT-GET-F-NO-INSTALL-RECOMMENDS"
                            },
                            {
                                "children": [
                                    {
                                        "children": [],
                                        "type": "SC-APT-GET-PACKAGE:CA-CERTIFICATES"
                                    },
                                    {
                                        "children": [],
                                        "type": "SC-APT-GET-PACKAGE:P11-KIT"
                                    }
                                ],
                                "type": "SC-APT-GET-PACKAGES"
                            }
                        ],
                        "type": "SC-APT-GET-INSTALL"
                    },
                    {
                        "children": [
                            {
                                "children": [],
                                "type": "SC-RM-F-RECURSIVE"
                            },
                            {
                                "children": [],
                                "type": "SC-RM-F-FORCE"
                            },
                            {
                                "children": [
                                    {
                                        "children": [
                                            {
                                                "children": [
                                                    {
                                                        "children": [
                                                            {
                                                                "type": "ABS-MAYBE-PATH",
                                                                "children": []
                                                            },
                                                            {
                                                                "type": "ABS-APT-LISTS",
                                                                "children": []
                                                            },
                                                            {
                                                                "type": "ABS-PATH-VAR",
                                                                "children": []
                                                            },
                                                            {
                                                                "type": "ABS-PATH-ABSOLUTE",
                                                                "children": []
                                                            }
                                                        ],
                                                        "type": "BASH-LITERAL"
                                                    },
                                                    {
                                                        "children": [
                                                            {
                                                                "type": "ABS-GLOB-STAR",
                                                                "children": []
                                                            }
                                                        ],
                                                        "type": "BASH-GLOB"
                                                    }
                                                ],
                                                "type": "BASH-CONCAT"
                                            }
                                        ],
                                        "type": "SC-RM-PATH"
                                    }
                                ],
                                "type": "SC-RM-PATHS"
                            }
                        ],
                        "type": "SC-RM"
                    }
                ],
                "type": "BASH-SCRIPT"
            }
        ],
        "type": "DOCKER-RUN"





                    {
                        "children": [],
                        "type": "SC-APT-GET-UPDATE"
                    },
                    {
                        "children": [
                            {
                                "children": [],
                                "type": "SC-APT-GET-F-YES"
                            },
                            {
                                "children": [],
                                "type": "SC-APT-GET-F-NO-INSTALL-RECOMMENDS"
                            },
                            {
                                "children": [
                                    {
                                        "children": [],
                                        "type": "SC-APT-GET-PACKAGE:CA-CERTIFICATES"
                                    },
                                    {
                                        "children": [],
                                        "type": "SC-APT-GET-PACKAGE:P11-KIT"
                                    }
                                ],
                                "type": "SC-APT-GET-PACKAGES"
                            }
                        ],
                        "type": "SC-APT-GET-INSTALL"
                    },


    ['SC-SET', 'SC-SET-F-E']
    ['SC-SET', 'SC-SET-F-U']
    ['SC-SET', 'SC-SET-F-X']
    ['SC-APT-GET-UPDATE']
    ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-YES']
    ['SC-APT-GET-INSTALL', 'SC-APT-GET-F-NO-INSTALL-RECOMMENDS']
    ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:CA-CERTIFICATES']
    ['SC-APT-GET-INSTALL', 'SC-APT-GET-PACKAGES', 'SC-APT-GET-PACKAGE:P11-KIT']
    ['SC-RM', 'SC-RM-F-RECURSIVE']
    ['SC-RM', 'SC-RM-F-FORCE']
    ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-LITERAL', 'ABS-MAYBE-PATH']
    ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-LITERAL', 'ABS-APT-LISTS']
    ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-LITERAL', 'ABS-PATH-VAR']
    ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-LITERAL', 'ABS-PATH-ABSOLUTE']
    ['SC-RM', 'SC-RM-PATHS', 'SC-RM-PATH', 'BASH-CONCAT', 'BASH-GLOB', 'ABS-GLOB-STAR']
```