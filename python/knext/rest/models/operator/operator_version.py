# coding: utf-8

"""
    knext

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

#  Copyright 2023 Ant Group CO., Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
#  in compliance with the License. You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied.

import pprint
import re  # noqa: F401

import six

from knext.rest.configuration import Configuration


class OperatorVersion(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        "overview_id": "int",
        "main_class": "str",
        "file_path": "str",
        "version": "int",
    }

    attribute_map = {
        "overview_id": "overviewId",
        "main_class": "mainClass",
        "file_path": "filePath",
        "version": "version",
    }

    def __init__(
        self,
        overview_id=None,
        main_class=None,
        file_path=None,
        version=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """OperatorVersion - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._overview_id = None
        self._main_class = None
        self._file_path = None
        self._version = None
        self.discriminator = None

        self.overview_id = overview_id
        self.main_class = main_class
        self.file_path = file_path
        self.version = version

    @property
    def overview_id(self):
        """Gets the overview_id of this OperatorVersion.  # noqa: E501


        :return: The overview_id of this OperatorVersion.  # noqa: E501
        :rtype: int
        """
        return self._overview_id

    @overview_id.setter
    def overview_id(self, overview_id):
        """Sets the overview_id of this OperatorVersion.


        :param overview_id: The overview_id of this OperatorVersion.  # noqa: E501
        :type: int
        """
        if (
            self.local_vars_configuration.client_side_validation and overview_id is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `overview_id`, must not be `None`"
            )  # noqa: E501

        self._overview_id = overview_id

    @property
    def main_class(self):
        """Gets the main_class of this OperatorVersion.  # noqa: E501


        :return: The main_class of this OperatorVersion.  # noqa: E501
        :rtype: str
        """
        return self._main_class

    @main_class.setter
    def main_class(self, main_class):
        """Sets the main_class of this OperatorVersion.


        :param main_class: The main_class of this OperatorVersion.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and main_class is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `main_class`, must not be `None`"
            )  # noqa: E501

        self._main_class = main_class

    @property
    def file_path(self):
        """Gets the file_path of this OperatorVersion.  # noqa: E501


        :return: The file_path of this OperatorVersion.  # noqa: E501
        :rtype: str
        """
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        """Sets the file_path of this OperatorVersion.


        :param file_path: The file_path of this OperatorVersion.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and file_path is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `file_path`, must not be `None`"
            )  # noqa: E501

        self._file_path = file_path

    @property
    def version(self):
        """Gets the version of this OperatorVersion.  # noqa: E501


        :return: The version of this OperatorVersion.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this OperatorVersion.


        :param version: The version of this OperatorVersion.  # noqa: E501
        :type: int
        """
        if (
            self.local_vars_configuration.client_side_validation and version is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `version`, must not be `None`"
            )  # noqa: E501

        self._version = version

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, OperatorVersion):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OperatorVersion):
            return True

        return self.to_dict() != other.to_dict()
