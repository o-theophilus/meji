<script>
	import { module } from '$lib/store';

	import Card from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';
	import Meta from '$lib/meta.svelte';

	import Delete from './delete.svelte';
	import Password from './password.svelte';
</script>

<Meta title="Setting" description="Setting" />

<Card>
	<Title title="Settings" />
	<Body>
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
	</Body>
</Card>
