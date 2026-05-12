<script>
	import { EmailTemplate } from '$lib/layout';
</script>

<EmailTemplate>
	<b> Dear {'{'}name{'}'}, </b>
	<br />
	<br />
	Use the code below to confirm your email change.
	<br />
	<br />
	<div
		style="
		text-align: center;
		font-size: x-large;
		padding: 16px;
		border: 2px solid #efefef;
		border-radius: 4px;
	"
	>
		<b> {'{'}code{'}'} </b>
	</div>
	<br />
	This code is valid for a limited time. If you didn't request this, you can safely ignore this email.
	<br /> <br />
	<b>Meji</b>
</EmailTemplate>
