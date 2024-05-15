<script>
	import BRound from '$lib/button/round.svelte';
</script>

<div class="block">
	<BRound
		icon="whatsapp"
		extra="outline"
		large
		href="https://wa.me/2349113717298/?text=Hello%20Meji.ng"
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
</div>

<style>
	.block {
		display: flex;
		gap: var(--sp1);
	}
</style>
