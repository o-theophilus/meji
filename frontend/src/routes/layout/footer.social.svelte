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

	<BRound icon="twitter" extra="outline" large href="https://twitter.com/meji_ng" target="_blank" />

	<BRound
		icon="facebook"
		extra="outline"
		large
		href="https://web.facebook.com/profile.php?id=61559751445797"
		target="_blank"
	/>
	<!-- href="https://m.facebook.com/o.theophilus" -->
</div>

<style>
	.block {
		display: flex;
		gap: var(--sp1);
	}
</style>
