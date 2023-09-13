<script>
	import { toast, loading } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Card from '$lib/card.svelte';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'please enter your name';
		}
		if (!form.email) {
			error.email = 'please enter your name';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'please enter a valid email address';
		}
		if (!form.message) {
			error.message = 'please enter your message';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/contact`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$toast = {
				status: 200,
				message: 'Message Sent'
			};
		} else {
			error = resp.error;
		}
	};
</script>

<div id="contact" />
<Card>
	<b>Contact us</b>
	<br />
	<br />
	<p>This is the 'contact' page. There's not much here.</p>
	<p>
		Feel free to contact us with questions or anything else. we will do our best to respond to all
		emails, although it may not be immediately.<br />
		<br />
		You can also contact us on:<br />
		Email: connekt.apps@gmail.com<br />
		Twitter: @connekt_app<br />
		<br />
		Please enter your contact details and a message below and we will try to answer your query as soon
		as possible.
	</p>
	<br />
	<br />
	<form on:submit|preventDefault novalidate autocomplete="off">
		<IG name="name" label="Fullname" {error} let:id>
			<input bind:value={form.name} {id} type="text" placeholder="Fullname here" />
		</IG>

		<IG name="email" {error} let:id>
			<input bind:value={form.email} {id} type="email" placeholder="Email here" />
		</IG>

		<IG name="phone" {error} let:id>
			<input bind:value={form.phone} {id} type="tel" placeholder="Phone number here" />
		</IG>

		<IG name="message" {error} let:id>
			<textarea bind:value={form.message} {id} placeholder="Message here" />
		</IG>

		{#if error.error}
			<p class="error">
				{error.error}
			</p>
			<br />
		{/if}
		<Button class="primary" on:click={validate}>Submit</Button>
	</form>
</Card>
