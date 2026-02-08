<script>
	import Form from './form.svelte';
	import Contact from './contact.svelte';
	import { Content } from '$lib/layout';
	import { Button } from '$lib/button';
</script>

<Content>
	<div class="form_area">
		<div class="left">
			<div class="page_title">Get In Touch</div>
			<br />
			Got a question or proposal, or just want to say hello? Please go ahead.

			<br />
			<br />
			<Contact></Contact>
		</div>
		<div class="form">
			<Form></Form>
		</div>
	</div>
</Content>

<style>
	.form_area {
		display: flex;
		flex-direction: column;
		gap: 42px;

		& .left,
		& .form {
			width: 100%;
		}
	}

	@media screen and (min-width: 580px) {
		.form_area {
			flex-direction: unset;
		}
	}
</style>
