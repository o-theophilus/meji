<script>
	import Card from '$lib/card.svelte';
	import Title from '$lib/title.svelte';
	import Form from './contact.form.svelte';
</script>

<div id="contact" />
<Card>
	<Title card>Contact us</Title>

	<section>
		Feel free to contact us with questions or anything else. we will respond to all enquires.
		<br />
		<br />
		<br />
		<Form />
	</section>
</Card>

<style>
	section {
		max-width: 512px;
	}

	@media screen and (min-width: 800px) {
	}
</style>
