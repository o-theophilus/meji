<script>
	import Group from '$lib/comp/card.svelte';
	import Title from '$lib/comp/card_title.svelte';
	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';

	import { page } from '$app/stores';
</script>

<svelte:head>
	<title>{$page.status} Error | Meji</title>
</svelte:head>

<Group>
	<Title title="{$page.status} Error" />
	<Body>
		{@html $page.error.message}

		<Button
			name="Home"
			icon="home"
			on:click={() => {
				document.location = '/';
			}}
		/>
	</Body>
</Group>
