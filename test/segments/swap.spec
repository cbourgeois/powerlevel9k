#!/usr/bin/env zsh
#vim:ft=zsh ts=2 sw=2 sts=2 et fenc=utf-8

# Required for shunit2 to run correctly
setopt shwordsplit
SHUNIT_PARENT=$0

function setUp() {
  export TERM="xterm-256color"
  # Load Powerlevel9k
  source powerlevel9k.zsh-theme

  # Initialize icon overrides
  _powerlevel9kInitializeIconOverrides

  # Precompile the Segment Separators here!
  _POWERLEVEL9K_LEFT_SEGMENT_SEPARATOR="$(print_icon 'LEFT_SEGMENT_SEPARATOR')"
  _POWERLEVEL9K_LEFT_SUBSEGMENT_SEPARATOR="$(print_icon 'LEFT_SUBSEGMENT_SEPARATOR')"
  _POWERLEVEL9K_LEFT_SEGMENT_END_SEPARATOR="$(print_icon 'LEFT_SEGMENT_END_SEPARATOR')"
  _POWERLEVEL9K_RIGHT_SEGMENT_SEPARATOR="$(print_icon 'RIGHT_SEGMENT_SEPARATOR')"
  _POWERLEVEL9K_RIGHT_SUBSEGMENT_SEPARATOR="$(print_icon 'RIGHT_SUBSEGMENT_SEPARATOR')"

  # Disable TRAP, so that we have more control how the segment is build,
  # as shUnit does not work with async commands.
  trap WINCH

  P9K_HOME=$(pwd)
  ### Test specific
  # Create default folder and git init it.
  FOLDER=/tmp/powerlevel9k-test/swap-test
  mkdir -p "${FOLDER}"
  cd $FOLDER
}

function tearDown() {
  # Go back to powerlevel9k folder
  cd "${P9K_HOME}"
  # Remove eventually created test-specific folder
  rm -fr "${FOLDER}"
  # At least remove test folder completely
  rm -fr /tmp/powerlevel9k-test
  p9k_clear_cache
}

function testSwapSegmentWorksOnOsx() {
    sysctl() {
        echo "vm.swapusage: total = 3072,00M  used = 1620,50M  free = 1451,50M  (encrypted)"
    }

    export OS="OSX"

    prompt_swap "left" "1" "false"
    p9k_build_prompt_from_cache

    assertEquals "%K{yellow} %F{black%}SWP%f %F{black}1.58G %k%F{yellow}%f " "${PROMPT}"

    unset OS
    unfunction sysctl
}

function testSwapSegmentWorksOnLinux() {
    mkdir proc
    echo "SwapTotal: 1000000" > proc/meminfo
    echo "SwapFree: 1000" >> proc/meminfo

    export OS="Linux"

    prompt_swap "left" "1" "false" "${FOLDER}"
    p9k_build_prompt_from_cache

    assertEquals "%K{yellow} %F{black%}SWP%f %F{black}0.95G %k%F{yellow}%f " "${PROMPT}"

    unset OS
}

source shunit2/source/2.1/src/shunit2