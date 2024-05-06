<script>
	import { module } from '$lib/store';

	import Card from '$lib/card.svelte';
	import Title from '$lib/title.svelte';
	import Button from '$lib/button/button.svelte';
	import Meta from '$lib/meta.svelte';
	import Center from '$lib/center.svelte';
	import Back from '$lib/button/back.svelte';

	import Delete from './_delete.svelte';
	import Password from './_password.svelte';
</script>

<Meta title="Setting" description="Setting" />

<Center>
	<Title>
		<svelte:fragment slot="left">
			<Back />
		</svelte:fragment>
		Settings
	</Title>
</Center>

<Card>
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

<style>
</style>
