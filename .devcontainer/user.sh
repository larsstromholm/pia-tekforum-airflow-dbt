#!/usr/bin/env bash

# Current User ID exists
echo "Checking username/group/id"
if id -nu ${USER_UID} > /dev/null 2>&1; then
    current_user_name="$(id -nu ${USER_UID})"
    echo "User id ${USER_UID} is already used by ${current_user_name}, changing the login to ${USERNAME}"
    usermod --login ${USERNAME} ${current_user_name}
fi

# Current user name exists
if id -u ${USERNAME} > /dev/null 2>&1; then
    current_group_name="$(id -gn ${USERNAME})"
    echo "Account ${USERNAME} already exists and is a member of the group ${current_group_name}"
    echo "Updating the group name from ${current_group_name} to ${USERNAME} and its id to ${USER_GID}"
    groupmod --gid ${USER_GID} --new-name ${USERNAME} ${current_group_name}
    echo "Updating the user ${USERNAME} to have uid ${USER_UID}, gid to ${USER_GID} and home to ${HOME}"
    usermod -s /bin/zsh --uid ${USER_UID} --gid ${USER_GID} --home ${HOME} -m ${USERNAME}
else
    echo "User account doesn't exist, creating its group first with name ${USERNAME} and id ${USER_GID}"
    groupadd --gid ${USER_GID} ${USERNAME}
    echo "Creating the user ${USERNAME} to have uid ${USER_UID}, gid ${USER_GID} and home ${HOME}"
    useradd -s /bin/zsh --uid ${USER_UID} --gid ${USER_GID} --home ${HOME} -m ${USERNAME}
fi

# add sudo support for non-root user
echo "Adding ${USERNAME} to sudoers"
echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME}
chmod 0440 /etc/sudoers.d/${USERNAME}
