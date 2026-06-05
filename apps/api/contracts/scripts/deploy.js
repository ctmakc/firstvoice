const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  const relayerAddress = process.env.RELAYER_ADDRESS || deployer.address;

  console.log("Deploying with account:", deployer.address);
  console.log("Relayer address:", relayerAddress);

  const SoulboundProvenance = await hre.ethers.getContractFactory("SoulboundProvenance");
  const contract = await SoulboundProvenance.deploy(relayerAddress);

  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("SoulboundProvenance deployed to:", address);
  console.log("Run the following to save the address:");
  console.log(`export PROVENANCE_CONTRACT_ADDRESS=${address}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
