/*
 * easykey.cpp
 *
 * simple keyboard input commands
 * 
 * (C) 2021/22 Christian Bergschneider & Stefan Fuss
 * 
 */
 
#include <stdint.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>

#include "easykey.h"

bool enterSomething( const char *prompt, char *s, uint16_t size, bool hidden, int (*validChar)( int ch ) ) {

  char ch;
  char *str = (char *) calloc( size, sizeof(char) );
  uint8_t i = 0;
  
  printf(prompt);

  while (1) {

    // vTaskDelay( 25 / portTICK_PERIOD_MS );
    
    ch = getchar();

    switch (ch) {
      
      case '\n': strcpy( s, str );
                 free(str);
                 putchar('\n');
                 return true;        
      
      case '\b': 
      case 127:  if (i>0) { 
                   str[--i] = '\0'; 
                   putchar( 127 ); 
                 }
                 break;
      
      case '\e': free(str);
                 putchar('\n');
                 return false;
      
      default:   if ( ( ch < 255 ) && ( validChar( ch ) ) && ( i<size-1) ) {
                   // add printable char
                   (hidden)?putchar( '*' ):putchar( ch );
                   str[i++] = ch;
                 }
                 break;
    }

  }
  
}

int printable( int ch ) {
  return (ch>=32) && (ch <= 126);
}

void enterString( const char *prompt, char *s, uint16_t size, bool hidden ) {

  if (!enterSomething( prompt, s, size, hidden, printable ) ) s[0] = '\0';
  
}

int identifier( int ch ) {
  return isdigit(ch) || isalpha(ch);
}

void enterIdentifier( const char *prompt, char *s, uint16_t size ) {

  if (!enterSomething( prompt, s, size, false, identifier ) ) s[0] = '\0';
  
}

uint16_t enterNumber( const char *prompt, uint16_t defaultValue, uint16_t minValue, uint16_t maxValue ) {

  char str[6];
  uint16_t i;

  while (1) {

    // get number and check on defaults
    if ( ( !enterSomething( prompt, str, 6, false, isdigit ) ) || ( str[0] == '\0' ) ) {
      i = defaultValue;
    } else {
      i = atoi( str );
    }

    // in range?
    if ( ( i >= minValue ) && ( i <= maxValue ) ) return i;

  }

}

int YN( int ch ) {
  return ( ch == 'Y' ) || ( ch == 'y' ) || ( ch == 'N' ) || ( ch == 'n' ) ;
}

bool yesNo( const char *prompt, bool defaultValue ) {

  char str[2];
  if ( (!enterSomething( prompt, str, 2, false, YN ) ) || ( strlen( str ) == 0 ) ) return defaultValue;

  return ( str[0] == 'y' ) || ( str[0] == 'Y' ) ;

}
