<script>
	import { RoundButton } from '$lib/button';

	let { show_password = $bindable() } = $props();
	console.log(show_password);
	// TODO: fix this now swapping
</script>

<form onsubmit={(e) => e.preventDefault()}>
	<RoundButton
		icon={show_password ? 'eye' : 'eye-off'}
		extra="hover_red"
		tabindex="-1"
		onclick={() => {
			console.log(1);

			show_password = !show_password;
		}}
	/>
</form>

<style>
	form {
		display: flex;
		align-items: center;

		height: 100%;
	}
</style>
