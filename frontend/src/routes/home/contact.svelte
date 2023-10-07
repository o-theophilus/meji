<script>
	import Card from '$lib/card.svelte';
	import Form from './contact.form.svelte';
	import Contact from './contact.contact.svelte';
	import Social from './contact.social.svelte';
</script>

<div id="contact" />
<Card>
	<div class="ctitle">Contact us</div>

	<br />
	<br />
	<section>
		<div>
			Feel free to contact us with questions or anything else. we will respond to all enquires.<br
			/>

			<div class="up">
				<br />
				<Contact />
				<br />
				<br />
				<Social />
			</div>
		</div>
		<div>
			<Form />
			<div class="down">
				<br />
				<br />
				<Contact />
				<br />
				<br />
				<Social />
			</div>
		</div>
	</section>
</Card>

<style>
	section {
		display: flex;
		flex-direction: column;
		gap: var(--sp4);
	}
	section > * {
		width: 100%;
	}

	.up {
		display: none;
	}

	@media screen and (min-width: 800px) {
		section {
			flex-direction: unset;
		}
		.up {
			display: unset;
		}
		.down {
			display: none;
		}
	}
</style>
