<script>
	import Form from './form.svelte';
	import Contact from './contact.svelte';
	import { Content } from '$lib/layout';
	import { Radio, Toggle } from '$lib/button';
</script>

<Content>
	<Toggle state_1="heool"></Toggle>

	<div class="toggle">
		<Radio list={['', 'orange', 'yellow']} onclick={(e) => console.log(e)}></Radio>
	</div>

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
	.toggle {
		--button-padding-x: 4px;
		--button-height: 22px;
		--button-border-radius: 50px;
	}

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
