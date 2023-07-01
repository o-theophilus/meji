<script>
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

		// if (Object.keys(err).length === 0) {
		// 	submit();
		// }
	};

	let sent = 0;
	const submit = async () => {
		sent = 1;
		const _resp = await fetch('https://formspree.io/f/xknkjbpb', {
			method: 'post',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(form)
		});

		let resp = await _resp.json();

		if (_resp.ok) {
			sent = 2;
		} else {
			sent = 0;
			error.form = resp.message;
		}
	};
</script>

<svelte:head>
	<title>Contact | Meji</title>
</svelte:head>

<h1>Contact us</h1>
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
<form on:submit|preventDefault={validate} novalidate autocomplete="off">
	<div class="ig ig--field">
		<label for="name"> Fullname: </label>
		<input type="text" bind:value={form.name} id="name" placeholder="Your fullname here" />
		{#if error.name}
			<p class="error">
				{error.name}
			</p>
		{/if}
	</div>

	<div class="ig ig--field">
		<label for="email"> Email: </label>
		<input type="email" bind:value={form.email} id="email" placeholder="Your email here" />
		{#if error.email}
			<p class="error">
				{error.email}
			</p>
		{/if}
	</div>
	<div class="ig ig--field">
		<label for="phone"> Phone: </label>
		<input type="tel" bind:value={form.phone} id="phone" placeholder="Your phone here" />
	</div>
	<div class="ig ig--field">
		<label for="message"> Message: </label>
		<textarea id="message" bind:value={form.message} placeholder="Your message here" />
		{#if error.message}
			<p class="error">
				{error.message}
			</p>
		{/if}
	</div>

	<div class="ig ig--button">
		<input type="submit" value="Send Message" />
	</div>
</form>
