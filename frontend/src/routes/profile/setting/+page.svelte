<script>
	import { module } from '$lib/store';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Meta from '$lib/meta.svelte';

	import Delete from './delete.svelte';
	import Password from './password.svelte';
</script>

<Meta title="Setting" description="Setting" />

<Card>
	<b> Settings </b>
	<br />
	<br />
	<Button
		name="Change Password"
		on:click={() => {
			$module = { module: Password };
		}}
	/>

	<Button
		name="Delete Account"
		on:click={() => {
			$module = { module: Delete };
		}}
	/>
</Card>
