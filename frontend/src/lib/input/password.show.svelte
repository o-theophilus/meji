<script>
	import { RoundButton } from '$lib/button';

	let { show_password = $bindable() } = $props();
	let icon = $derived(show_password ? 'eye' : 'eye-off');
</script>

<form onsubmit={(e) => e.preventDefault()}>
	<RoundButton
		icon={show_password ? 'eye' : 'eye-off'}
		extra="hover_red"
		tabindex="-1"
		onclick={() => {
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
