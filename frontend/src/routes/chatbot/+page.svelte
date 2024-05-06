<script>
	import Meta from '$lib/meta.svelte';
	import Center from '$lib/center.svelte';
	import Card from '$lib/card.svelte';
	import Title from '$lib/title.svelte';

	import Button from '$lib/button/tag.svelte';
</script>

<Meta title="ChatBot" description="ChatBot" />

<Center>
	<Title>ChatBot</Title>
</Center>

<Card>
	<Button primary size="">hello</Button>
	<br />
	<br />
	<Button extra="" size="large">hello</Button>
</Card>

<style>
</style>
