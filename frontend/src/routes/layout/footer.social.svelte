<script>
	import BRound from '$lib/button/round.svelte';
</script>

<div class="block">
	<BRound
		icon="whatsapp"
		extra="outline"
		large
		href="https://wa.me/2348067397793/?text=Hello%20Theophilus"
		target="_blank"
	/>

	<BRound
		icon="twitter"
		extra="outline"
		large
		href="https://twitter.com/o__theophilus"
		target="_blank"
	/>

	<BRound
		icon="facebook"
		extra="outline"
		large
		href="https://m.facebook.com/o.theophilus"
		target="_blank"
	/>

	<!-- <BRound extra=outline large href="https://www.instagram.com/o_theophilus_/" target="_blank" rel="noopener noreferrer"		icon="instagram" >
	</BRound> -->
</div>

<style>
	.block {
		display: flex;
		gap: var(--sp1);
	}
</style>
