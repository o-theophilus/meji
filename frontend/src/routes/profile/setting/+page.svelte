<script>
	import { module } from '$lib/store';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';
	import Meta from '$lib/meta.svelte';

	import Delete from './_delete.svelte';
	import Password from './_password.svelte';
</script>

<Meta title="Setting" description="Setting" />

<Card>
	<b> Settings </b>
	<br />
	<br />
	<Button
		on:click={() => {
			$module = { module: Password };
		}}
	>
		Change Password
	</Button>
	<br />
	<Button
		on:click={() => {
			$module = { module: Delete };
		}}
	>
		Delete Account
	</Button>
</Card>
