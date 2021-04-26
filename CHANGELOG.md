# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Extrapolation and interpolation of data received from the server using the UDP protocol in order to reduce latency, so that the server can send data to the client less frequently and the player's movement is still smooth.
### Changed
- Correct the extrapolation and interpolation code to make it more scalable.


## [0.1] - 2021-04-18
### Added
- sending client input status from client to server using UDP protocol
- sending server output like the player's position using the UDP protocol
- Creating a new player object after client join on client and server side
- Delete player object after client disconect on client and server side
- Chat using TCP protocol
- Integration with the Arcade library

[Unreleased]: https://github.com/stanik120/Multiplayer-Arcade/compare/v0.1...HEAD
<!-- [0.0.2]: https://github.com/stanik120/Multiplayer-Arcade/compare/v0.1...v0.2 -->
[0.1]: https://github.com/stanik120/Multiplayer-Arcade/releases/tag/v0.1