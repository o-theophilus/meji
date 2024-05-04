<script>
	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';
</script>

<div class="block">
	<BRound size="large" href="https://wa.me/2348067397793/?text=Hello%20Theophilus" target="_blank">
		<SVG type="whatsapp" />
	</BRound>

	<BRound size="large" href="https://twitter.com/o__theophilus" target="_blank">
		<SVG type="twitter" />
	</BRound>

	<BRound size="large" href="https://m.facebook.com/o.theophilus" target="_blank">
		<SVG type="facebook" />
	</BRound>

	<!-- <BRound size="large" href="https://www.instagram.com/o_theophilus_/" target="_blank" rel="noopener noreferrer">
		<SVG type="instagram" />
	</BRound> -->
</div>

<style>
	.block {
		display: flex;
		gap: var(--sp1);
	}
</style>
