/*
 * Demonstration Platform - Home Page
 * ===================================
 * Educational Demo – OAuth Token Theft Simulation
 * 
 * This page redirects to the login page.
 */

import { redirect } from 'next/navigation'

export default function Home() {
  redirect('/login')
}
